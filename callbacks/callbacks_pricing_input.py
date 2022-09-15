__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import io
import os
import time
import uuid
import dash
import base64
import urllib
import logging
import pandas as pd
from dash import dcc
from dash.dependencies import Input, Output, State
from sqlalchemy import exc as sqlalchemy_exc
from callback_manager import CallbackManager
from tasks import long_running_simulation, long_running_simulation_celery
from datasets.backend import df_consolidated, df_features, df_variable_type, df_xvar, \
                            df_seasonality, dict_parent_category_id_map, dict_product_category_id_map, dict_product_id_map, \
                            dict_shop_id_map, lt_month_range, lt_month2week_list, st_month_range, st_month2week_list
from utility.utility_data_transformation import custom_datepicker
from utility.utility_tasks import TaskUploadModel

logger = logging.getLogger('pricing_handler') # Retrieve Logger Handler
callback_manager = CallbackManager()

#region Pricing Input
@callback_manager.callback([Output(component_id='datatable-input', component_property='data'),
                            Output(component_id='datatable-input', component_property='columns')],
                            [Input(component_id='dd-period', component_property='value'),
                            Input(component_id='dpr-period', component_property='start_date'),
                            Input(component_id='dpr-period', component_property='end_date'),
                            Input(component_id='dd-parent-product-category', component_property='value'),
                            Input(component_id='dd-product-category', component_property='value'),
                            Input(component_id='dd-product-name', component_property='value'),
                            Input(component_id='dd-shop-name', component_property='value'),
                            Input(component_id='upload-data', component_property='contents'),
                            Input(component_id='btn-reset-simulator', component_property='n_clicks')],
                            State(component_id='storage-pricing-input', component_property='data'))
def set_simulation_input_data(period_type, custom_start_date, custom_end_date, sel_parent_product_category, sel_product_category, \
                            sel_product, sel_shop, uploaded_content, n_reset_simulator, stored_pricing_input):
    
    # If upload input is selected
    if uploaded_content is not None:
        decoded = base64.b64decode(uploaded_content.split(",")[1])
        df_templatedata = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        column_list = []
        for column_name in df_templatedata.columns:
            if column_name in ['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']:
                column_list.append({"name": column_name, "id": column_name, 'editable': False})
            else:
                column_list.append({"name": column_name, "id": column_name})
        return df_templatedata.to_dict("records"), column_list
    
    # Generate Consolidated DF based on Category, Product and Shop selected
    if period_type.__eq__('Quarterly'):
        RSP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=st_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=st_month2week_list)])
    elif period_type.__eq__('Annually'):
        RSP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=lt_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=lt_month2week_list)])
    elif period_type.__eq__('Custom'):
        cdr_month_range, cdr_week_range = custom_datepicker(start_date=custom_start_date, end_date=custom_end_date)
        RSP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=cdr_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=cdr_week_range)])

    # Check for None type parent product category, product category, product and shop
    if sel_parent_product_category is None or len(sel_parent_product_category) == 0:
        sel_parent_product_category = [parent_cat for parent_cat in df_consolidated.PARENT_CATEGORY]
    if sel_product_category is None or len(sel_product_category) == 0:
        sel_product_category = [product_cat for product_cat in df_consolidated.PRODUCT_CATEGORY]
    if sel_product is None or len(sel_product) == 0:
        sel_product = [product for product in df_consolidated.PRODUCT]
    if sel_shop is None or len(sel_shop) == 0:
        sel_shop = [shop for shop in df_consolidated.SHOP]

    # Table structure for RSP and TMP with default price across period rounded off to 3 decimals
    RSP_structure['PRICE_PER_ITEM'] = RSP_structure['PRICE_PER_ITEM'].map("{:.2f}".format)
    TMP_structure['PRICE_PER_ITEM'] = TMP_structure['PRICE_PER_ITEM'].map("{:.2f}".format)
    RSP_default = RSP_structure.ffill(axis = 1)
    TMP_default = TMP_structure.ffill(axis = 1)
    
    # Default structure
    if period_type.__eq__('Quarterly'):
        temp_default = TMP_default
    elif period_type.__eq__('Annually'):
        temp_default = RSP_default
    elif period_type.__eq__('Custom'):
        temp_default = TMP_default

    temp_mask = (temp_default.PARENT_CATEGORY.isin(sel_parent_product_category)) & \
                (temp_default.PRODUCT_CATEGORY.isin(sel_product_category))  & \
                (temp_default.PRODUCT.isin(sel_product)) & \
                (temp_default.SHOP.isin(sel_shop))
    df_templatedata = temp_default.loc[temp_mask, :]

    # Sorting Table with respect to combination of Province, Manuf and Brand
    df_templatedata = df_templatedata.sort_values(by=['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP']).reset_index(drop=True)

    column_list = []
    for column_name in df_templatedata.columns:
        if column_name in ['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']:
            column_list.append({"name": column_name, "id": column_name, 'editable': False})
        else:
            column_list.append({"name": column_name, "id": column_name})
    return df_templatedata.to_dict('records'), column_list

# Download template link
@callback_manager.callback(Output(component_id='download-pricing-csv', component_property='data'),
                        Input(component_id='btn-template-pricing', component_property='n_clicks'),
                        State(component_id='datatable-input', component_property='data'))
def download_template_link(on_click, tbdata):
    if on_click is not None and len(tbdata)>0:
        oritemplate = pd.DataFrame(data = tbdata)
        return dcc.send_data_frame(oritemplate.to_csv, "pricing_template.csv", index=False)
#endregion

#region Running Simulations via rabbitmq message broker + celery worker
@callback_manager.callback([Output(component_id='task-label', component_property='children'),
                        Output(component_id='task-section', component_property='style')],
                        Input(component_id='btn-run-simulation', component_property='n_clicks'),
                        [State(component_id='dd-period', component_property='value'),
                        State(component_id='datatable-input', component_property='data'),
                        State(component_id='text-scenario-name', component_property='value'),
                        State(component_id='storage-username', component_property='data')])
def run_prediction(n_run_simulation, period_type, pricing_input, scenario_name, user_name):
    # Identification of Triggering Point
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_component_id = 'No clicks yet'  
    else:
        trigger_component_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Conditional Output wrt Input Source Type
    if trigger_component_id == 'btn-run-simulation' and n_run_simulation:
        from app import app, engine, tasks_tbl, uploaded_path 
        print('Run Simulation button clicked')
        logger.info('Run Simulation button clicked')
        
        # Extracting input pricing table data
        df_pricing_input = pd.DataFrame(data=pricing_input)
        
        # COMMENTED FOR NOW and replaced with empty dataframe
        df_historic = pd.DataFrame()
        # df_benchmarking_preds = baseline_predictions_weekly if period_type.__eq__('Quarterly') or period_type.__eq__('Custom') else baseline_predicitons_monthly
        df_benchmarking_preds = pd.DataFrame()
        df_competitor_rank = pd.DataFrame()
        df_seasonality_weather = df_seasonality.copy()
        df_switching = pd.DataFrame()
        df_models = pd.DataFrame()

        # Generate DB placeholder with unique UUID
        logger.info('Generating database placeholder with unique id started')
        conn = engine.connect()
        db_task_id = str(uuid.uuid4())
        try:
            ins = tasks_tbl.insert().values(
                                        username=user_name, 
                                        dbtaskid=db_task_id,
                                        scenarioname=scenario_name,
                                        submissiondate=pd.to_datetime('today')
                                    )
            conn.execute(ins)
        except sqlalchemy_exc.SQLAlchemyError as ex:
            print(str(ex))
            logger.info('Generating database placeholder with unique id caught exception for database task id: %s as %s' %(db_task_id, str(ex)))
        conn.close()
        logger.info('Generating database placeholder with unique id ended')

        logger.info('Generating task upload model started')
        simulation_json_body, blob_data = None, None
        # Uploading files to local storage, zipping it and converting to blob / Generating simulation body
        try:
            task_uploader_instance = TaskUploadModel(
                df_historic=df_historic, 
                df_consolidated=df_consolidated, 
                df_benchmarking_preds=df_benchmarking_preds, 
                df_pricing_input=df_pricing_input, 
                df_features=df_features, 
                df_xvar=df_xvar, 
                df_competitor_rank=df_competitor_rank, 
                overridden_xvars_dict={'seasonality_weather_df':df_seasonality_weather}, 
                df_variable_type=df_variable_type, 
                df_switching=df_switching, 
                df_model_endpoints=df_models, 
                model_endpoints_dict=app.server.config['PRICING_MODEL_ENDPOINTS'], 
                model_picklefile_dict=app.server.config['PRICING_MODEL_PKLFILES'], 
                mapping_dict={'parent':dict_parent_category_id_map,
                            'parent_inv':{v:k for k,v in dict_parent_category_id_map.items()}, 
                            'category':dict_product_category_id_map, 
                            'category_inv':{v:k for k,v, in dict_product_category_id_map.items()},
                            'product':dict_product_id_map, 
                            'product_inv':{v:k for k,v, in dict_product_id_map.items()},
                            'shop':dict_shop_id_map,
                            'shop_inv':{v:k for k,v, in dict_shop_id_map.items()}}, 
                period_type=period_type,
                month_to_weeks=lt_month2week_list, 
                pickle_flag=True 
            )
            
            if task_uploader_instance.upload_files(upload_path=os.path.join(uploaded_path, db_task_id)):
                print('Files uploaded to static folder successfully for database task id: %s' %(db_task_id))
                logger.info('Files uploaded to static folder successfully for database task id: %s' %(db_task_id))
            else:
                print('Files uploaded to static folder caught exception for database task id: %s' %(db_task_id))
                logger.error('Files uploaded to static folder caught exception for database task id: %s' %(db_task_id))

            try:
                blob_data = task_uploader_instance.convert_to_blob(upload_path=os.path.join(uploaded_path, db_task_id)) 
                print('Files zipped and converted to blob for uplaoding to database for database task id: %s' %(db_task_id))
                logger.info('Files zipped and converted to blob for uplaoding to database for database task id: %s' %(db_task_id))
            except Exception:
                print('Files zipped and converted to blob for uplaoding to database caught exception for database task id: %s' %(db_task_id))
                logger.error('Files zipped and converted to blob for uplaoding to database caught exception for database task id: %s' %(db_task_id))
            
            logger.info('Generating message body started for database task id: %s' %(db_task_id))
            simulation_json_body = task_uploader_instance.generate_json()
            logger.info('Generating message body ended for database task id: %s' %(db_task_id))
        except Exception as ex:
            print(ex)
            pass
        logger.info('Generating task upload model ended')

        # Updating Table Row entry in DB with blob data
        logger.info('Updating database placeholder with blob data started for database task id: %s' %(db_task_id))
        try:
            update_query = tasks_tbl.update().where(
                                                tasks_tbl.c.dbtaskid==db_task_id and \
                                                tasks_tbl.c.username==username).values(
                                                                                    taskdata = blob_data     
                                                                                )
            conn.execute(update_query)
        except sqlalchemy_exc.SQLAlchemyError as ex:
            print(str(ex))
            logger.info('Updating database placeholder with blob data caught exception for database task id: %s as %s' %(db_task_id, str(ex)))
            pass
        logger.info('Updating database placeholder with blob data ended for database task id: %s' %(db_task_id))
            
        # Scheduling long running simulation tasks via celery and rabbitmQ
        simulation_task = long_running_simulation_celery.delay(
                                df_historic=df_historic.to_dict(),
                                df_consolidated=df_consolidated.to_dict(),
                                df_benchmarking_preds=df_benchmarking_preds.to_dict(),
                                df_pricing_input=df_pricing_input.to_dict(),
                                df_features=df_features.to_dict(),
                                df_xvar=df_xvar.to_dict(),
                                df_competitor_rank=df_competitor_rank.to_dict(),
                                overridden_xvars_dict={'seasonality_weather_df':df_seasonality_weather.to_dict()},
                                df_variable_type=df_variable_type.to_dict(),
                                df_switching=df_switching.to_dict(),
                                df_model_endpoints=df_models.to_dict(),
                                model_endpoints_dict=app.server.config['PRICING_MODEL_ENDPOINTS'],
                                model_picklefile_dict=app.server.config['PRICING_MODEL_PKLFILES'],
                                mapping_dict={'parent':dict_parent_category_id_map,
                                            'parent_inv':{v:k for k,v in dict_parent_category_id_map.items()}, 
                                            'category':dict_product_category_id_map, 
                                            'category_inv':{v:k for k,v, in dict_product_category_id_map.items()},
                                            'product':dict_product_id_map, 
                                            'product_inv':{v:k for k,v, in dict_product_id_map.items()},
                                            'shop':dict_shop_id_map,
                                            'shop_inv':{v:k for k,v, in dict_shop_id_map.items()}},
                                period_type=period_type,
                                month_to_weeks=lt_month2week_list,
                                pickle_flag=True
                            )
        # Task id of current celery task
        task_id = simulation_task.id
        time.sleep(0.5)  # Need a short sleep for task_id to catch up

        # Add this task id to the task db table
        task_status = simulation_task.state
        conn = engine.connect()
        try:
            ins = tasks_tbl.insert().values(
                                        username=user_name, 
                                        taskid=task_id, 
                                        taskstatus=task_status, 
                                        scenarioname=scenario_name,
                                        submissiondate=pd.to_datetime('today')
                                    )
            conn.execute(ins)
        except sqlalchemy_exc.SQLAlchemyError as ex:
            print(str(ex))
        conn.close()

        current_task_progress = 'Pricing Scenario submitted with Task ID: %s' %(str(task_id))
        return current_task_progress, {'display': 'block'}

'''
@callback_manager.callback([Output(component_id='storage-pricing-output', component_property='data'),
                        Output(component_id='storage-pricing-input', component_property='data')],
                        Input(component_id='btn-run-simulation', component_property='n_clicks'),
                        [State(component_id='dd-period', component_property='value'),
                        State(component_id='datatable-input', component_property='data'),
                        State(component_id='storage-pricing-output', component_property='data'),
                        State(component_id='storage-pricing-input', component_property='data')], prevent_initial_call=True)
def run_prediction(n_run_simulation, period_type, pricing_input, pricing_output_state, pricing_input_state):

    # Identification of Triggering Point
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_component_id = 'No clicks yet'  
    else:
        trigger_component_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Conditional Output wrt Input Source Type
    if trigger_component_id == 'btn-run-simulation' and n_run_simulation:
        from app import app
        print('Run Simulation Clicked')
        
        # Extracting input pricing table data
        df_pricing_input = pd.DataFrame(data=pricing_input)
        
        # COMMENTED FOR NOW and replaced with empty dataframe
        df_historic = pd.DataFrame()
        # df_benchmarking_preds = baseline_predictions_weekly if period_type.__eq__('Quarterly') or period_type.__eq__('Custom') else baseline_predicitons_monthly
        df_benchmarking_preds = pd.DataFrame()
        df_competitor_rank = pd.DataFrame()
        df_seasonality_weather = df_seasonality.copy()
        df_switching = pd.DataFrame()
        df_models = pd.DataFrame()

        # Scheduling long running simulation tasks via celery and rabbitmQ
        df_predicted = long_running_simulation(df_historic=df_historic,
                                            df_consolidated=df_consolidated,
                                            df_benchmarking_preds=df_benchmarking_preds,
                                            df_pricing_input=df_pricing_input,
                                            df_features=df_features,
                                            df_xvar=df_xvar,
                                            df_competitor_rank=df_competitor_rank,
                                            overridden_xvars_dict={'seasonality_weather_df':df_seasonality_weather},
                                            df_variable_type=df_variable_type,
                                            df_switching=df_switching,
                                            df_model_endpoints=df_models,
                                            model_endpoints_dict=app.server.config['PRICING_MODEL_ENDPOINTS'],
                                            model_picklefile_dict=app.server.config['PRICING_MODEL_PKLFILES'],
                                            mapping_dict={'parent':dict_parent_category_id_map,
                                                        'parent_inv':{v:k for k,v in dict_parent_category_id_map.items()}, 
                                                        'category':dict_product_category_id_map, 
                                                        'category_inv':{v:k for k,v, in dict_product_category_id_map.items()},
                                                        'product':dict_product_id_map, 
                                                        'product_inv':{v:k for k,v, in dict_product_id_map.items()},
                                                        'shop':dict_shop_id_map,
                                                        'shop_inv':{v:k for k,v, in dict_shop_id_map.items()}},
                                            period_type=period_type,
                                            month_to_weeks=lt_month2week_list,
                                            pickle_flag=True,
                                            logger=logger)
        return df_predicted.to_dict('records'), df_pricing_input.to_dict('records')

    elif trigger_component_id == 'datatable-input':
        if pricing_input_state is None and pricing_output_state is None:
            return pd.DataFrame().to_dict('records'), pd.DataFrame().to_dict('records')
        elif pricing_input_state is not None and pricing_output_state is not None:
            return pricing_output_state, pricing_input_state
'''
#endregion