__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import copy
import pandas as pd

from celery.result import AsyncResult
from sqlalchemy import exc as sqlalchemy_exc
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts import layout_retail_summary, layout_pricing_input, layout_pricing_sales, layout_pivot_kpis, layout_kpis
from tasks import celery_app
from datasets.backend import df_transactions, df_products, df_shops, df_product_categories, parent_product_categories

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='tabs-content', component_property='children'),
                        Input(component_id='tabs', component_property='value'))
def render_content(tab):
    if tab == 'tab-1':
        return layout_retail_summary.layout
    elif tab == 'tab-2':
        return layout_pricing_input.layout
    elif tab == 'tab-3':
        return layout_pricing_sales.layout
    elif tab == 'tab-4':
        return layout_pivot_kpis.layout
    elif tab == 'tab-5':
        return layout_kpis.layout

@callback_manager.callback([Output(component_id='btn-run-simulation', component_property='style'),
                        Output(component_id='btn-reset-simulator', component_property='style')],
                        Input(component_id='tabs', component_property='value'))
def render_button(tab):
    if tab == 'tab-2':
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'} 

@callback_manager.callback(Output(component_id='dd-parent-product-category', component_property='value'),
                        Input(component_id='chklist-product-selector', component_property='value'))
def set_parent_category_options(sel_all_values):
    if isinstance(sel_all_values, list) and 'sl_parentcategories' in sel_all_values:
        return [parent_category for parent_category in parent_product_categories]
    else:
        return no_update

@callback_manager.callback([Output(component_id='dd-product-category', component_property='options'),
                        Output(component_id='dd-product-category', component_property='value')],
                        [Input(component_id='dd-parent-product-category', component_property='value'),
                        Input(component_id='chklist-product-selector', component_property='value')])
def set_product_category_options(sel_parent_product_categories, sel_all_values):

    if isinstance(sel_parent_product_categories, list):
        # Condition for setting all product categories if none is selected
        if len(sel_parent_product_categories) == 0:
            sel_parent_product_categories = copy.deepcopy(parent_product_categories)

        sel_df_parent_product_categories = df_product_categories.loc[df_product_categories.parent_category_name.isin(sel_parent_product_categories)].reset_index(drop=True)

        # Extracting product names based on product categories
        product_category_mask = df_product_categories.item_category_id.isin(list(sel_df_parent_product_categories.item_category_id.unique()))
        sel_df_product_categories = df_product_categories.loc[product_category_mask].reset_index(drop=True)

        # Extracting final product options and setting default as first product
        final_options = sorted(list(sel_df_product_categories.translated_item_category_name.unique()))

        if (isinstance(sel_all_values, list) and 'sl_productcategories' in sel_all_values):
            # Condition which selects all product categories upon selection
            return final_options, [final_option for final_option in final_options]
        # elif (isinstance(sel_all_values, list) and 'sl_productcategories' not in sel_all_values):
        #     # Condition in which all porduct categories are not selected but some other checklist item is selected
        #     return final_options, no_update
        else:
            # Generic Condition irrespective of all product categories selection 
            return final_options, [final_options[0]]
    else:
        return no_update 
    
@callback_manager.callback([Output(component_id='dd-product-name', component_property='options'),
                        Output(component_id='dd-product-name', component_property='value')],
                        [Input(component_id='dd-product-category', component_property='value'),
                        Input(component_id='chklist-product-selector', component_property='value')])
def set_product_options(sel_product_categories, sel_all_values):
    if isinstance(sel_product_categories, list):
        # Condition for setting all product categories if none is selected
        if len(sel_product_categories) == 0:
            sel_product_categories = sorted(list(df_product_categories.translated_item_category_name.unique()))

        sel_df_product_categories = df_product_categories.loc[df_product_categories.translated_item_category_name.isin(sel_product_categories)].reset_index(drop=True)

        # Extracting product names based on product categories
        product_mask = df_products.item_category_id.isin(list(sel_df_product_categories.item_category_id.unique()))
        sel_df_product = df_products.loc[product_mask].reset_index(drop=True)

        # Extracting final product options and setting default as first product
        final_options = sorted(list(sel_df_product.translated_item_name.unique()))

        if (isinstance(sel_all_values, list) and 'sl_products' in sel_all_values):
            # Condition which selects all products upon selection
            return final_options, [final_option for final_option in final_options]
        # elif (isinstance(sel_all_values, list) and 'sl_products' not in sel_all_values):
        #     # Condition in which all products are not selected but some other checklist item is selected
        #     return final_options, no_update
        else:
            # Generic Condition irrespective of all products selection 
            return final_options, [final_options[0]]
    else:
        return no_update 

@callback_manager.callback([Output(component_id='dd-shop-name', component_property='options'),
                        Output(component_id='dd-shop-name', component_property='value')],
                        [Input(component_id='dd-product-name', component_property='value'),
                        Input(component_id='chklist-product-selector', component_property='value')],
                        State(component_id='dd-product-name', component_property='options'))
def set_product_options(sel_product_names, sel_all_values, avail_products):
    if isinstance(sel_product_names, list):
        # Condition for setting all products if none is selected
        if len(sel_product_names) == 0:
            sel_product_names = copy.deepcopy(avail_products)

        sel_df_product = df_products.loc[df_products.translated_item_name.isin(sel_product_names)].reset_index(drop=True)

        # Extracting shop ids based on product names
        shop_mask = df_transactions.item_id.isin(list(sel_df_product.item_id.unique()))
        sel_df_transactions = df_transactions.loc[shop_mask].reset_index(drop=True)

        # Extracting shop names based on extracted shop ids
        shop_id_list = sorted(list(sel_df_transactions.shop_id.unique()))
        sel_df_shop = df_shops.loc[df_shops.shop_id.isin(shop_id_list)].reset_index(drop=True)

        # Extracting final shop optons and setting default as first shop
        final_options = sorted(list(sel_df_shop.translated_shop_name.unique()))

        if (isinstance(sel_all_values, list) and 'sl_shops' in sel_all_values):
            # Condition which selects all shops upon selection
            return final_options, [final_option for final_option in final_options]
        # elif (isinstance(sel_all_values, list) and 'sl_shops' not in sel_all_values):
        #     # Condition in which all shops are not selected but some other checklist item is selected
        #     return final_options, no_update
        else:
            # Generic Condition irrespective of all shops selection 
            return final_options, [final_options[0]]
    else:
        return no_update

@callback_manager.callback([Output(component_id='simulation-detail', component_property='style'),
            Output(component_id='prediction-detail', component_property='style')],
            Input(component_id='tabs', component_property='value'))
def render_side_filter(tab):
    # Condition for hiding and displaying simualtion as well as prediction filters from sidepanel
    if tab == 'tab-2':
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        return simulation_detail_style, prediction_detail_style
    elif tab == 'tab-3':
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}
        return simulation_detail_style, prediction_detail_style
    else:
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        return simulation_detail_style, prediction_detail_style

@callback_manager.callback(Output(component_id='datatable-task', component_property='data'),
                        Input(component_id='task-monitor-interval', component_property='n_intervals'),
                        [State(component_id='storage-username', component_property='data'),
                        State(component_id='datatable-task', component_property='data')])
def refresh_task_table(n_int, username, task_state):
    try:
        from app import engine, tasks_tbl
        def extract_task_ids(u_name=username):
            conn = engine.connect()
            query = 'SELECT * FROM tasks WHERE username=\'%s\'' %(str(username))
            try:
                cursor= conn.execute(query)
                rows = cursor.fetchall()
            except sqlalchemy_exc.SQLAlchemyError as ex:
                print(ex)
                conn.close()
            conn.close()
            return rows

        task_list = extract_task_ids(u_name=username)
        if len(task_list) > 0:
            df_task = pd.DataFrame(columns=['task_id', 'pricing_scenario', 'task_status']) if task_state is None else \
                    pd.DataFrame(data=task_state)   
            conn = engine.connect()
            for task in task_list:
                task_id = task.taskid
                pricing_scenario_name = task.scenarioname

                celery_task = AsyncResult(id=task_id, app=celery_app)
                current_task_status = celery_task.state

                try:
                    # Updating Table Row entry in DB
                    update_query = tasks_tbl.update().where(
                                                        tasks_tbl.c.taskid==task_id and \
                                                        tasks_tbl.c.username==username).values(
                                                                                            taskstatus = current_task_status     
                                                                                        )
                    conn.execute(update_query)
                except sqlalchemy_exc.SQLAlchemyError as ex:
                    print(ex)
                    continue
                except Exception as ex:
                    print(ex)
                    continue

                try:
                    # Updating Table Row instance
                    if task_id not in list(df_task['task_id'].unique()):
                        # data_dict = {'task_id': task_id, 'pricing_scenario': pricing_scenario_name, 'task_status': current_task_status}
                        df_task = pd.concat([df_task, pd.DataFrame.from_dict(data={'task_id': [task_id], 'pricing_scenario': [pricing_scenario_name], 'task_status': [current_task_status]})], ignore_index=True)
                    else:
                        task_data = df_task.loc[df_task['task_id'].isin([task_id])]
                        df_task.iloc[task_data.index[0], df_task.columns.get_loc('task_status')] = current_task_status
                except Exception as ex:
                    print(ex)
            conn.close()
            return df_task.to_dict('records')
        else:
            return task_state
    except Exception as ex:
        print(ex)
        return task_state

@callback_manager.callback([Output(component_id='storage-pricing-output', component_property='data'),
                        Output(component_id='storage-pricing-input', component_property='data')],
                        Input(component_id='datatable-task', component_property='active_cell'),
                        [State(component_id='storage-username', component_property='data'),
                        State(component_id='datatable-task', component_property='data')])
def render_results(selected_cell, username, task_state):
    try:
        if task_state is None:
            return no_update
        else:
            from tasks import celery_app
            df_task = pd.DataFrame(columns=['task_id','task_status','open_scenario']) if task_state is None else \
                        pd.DataFrame(data=task_state)  
            selected_row_id = selected_cell['row'] if selected_cell else None
            selected_task_id = df_task.iloc[selected_row_id].task_id

            # Extract results from database
            extracted_task = AsyncResult(id=selected_task_id, app=celery_app)
            if extracted_task.state == 'SUCCESS':
                if 'result' in extracted_task.info:
                    extracted_task_result = extracted_task.info
                    df_predicted = pd.read_json(extracted_task_result.get('predicted_df')) if 'predicted_df' in extracted_task_result else {}
                    df_pricing = pd.read_json(extracted_task_result.get('pricing_df')) if 'pricing_df' in extracted_task_result else {}
                    return df_predicted.to_dict('records'), df_pricing.to_dict('records')
            else:
                return no_update, no_update

    except Exception as ex:
        print(ex)
        return no_update, no_update