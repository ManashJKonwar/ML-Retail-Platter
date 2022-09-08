__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
import json
import celery
import pandas as pd

from config.celerytasklogger import logger
from utility.utility_model_service import PredictSalesModel
from utility.utility_data_transformation import compile_prediction, custom_formatter

config_message_broker, config_db_server = None, None
try:
    with open(os.path.join('config','config_messagebrokers.json')) as config_file:
        config_message_broker = json.load(config_file)
except Exception as ex:
    print("Reading Message Broker Configuration raised an exception: "+str(ex))

try:
    with open(os.path.join('config','config_dbservers.json')) as config_file:
        config_db_server = json.load(config_file)
except Exception as ex:
    print("Reading DB Server Configuration raised an exception: "+str(ex))
os.environ['MESSAGE_BROKER'] = json.dumps(config_message_broker["rabbitmq_debug"]) if config_message_broker is not None else json.dumps({})
os.environ['DB_SERVER'] = json.dumps(config_db_server["redis_backend_debug"]) if config_db_server is not None else json.dumps({})

celery_app = celery.Celery('pricing_simulator')
celery_app.conf.update(
    # settings for message broker
    broker_url='amqp://%s:%s@localhost:%s/%s' %(json.loads(os.environ['MESSAGE_BROKER'])['username'],
                                                json.loads(os.environ['MESSAGE_BROKER'])['password'],
                                                json.loads(os.environ['MESSAGE_BROKER'])['port'],
                                                json.loads(os.environ['MESSAGE_BROKER'])['vhost']),
    # broker_url='redis://:dmkTkW9Y6SuxHHxHeyGegnlEIQdQqLN5Yr6xu75C+Js=@batcanadapricingdev.redis.cache.windows.net:6379/0', # BAT cache
    broker_pool_limit=1,
    broker_heartbeat=None,
    broker_connection_timeout=30,
    event_queue_expires=60,
    worker_prefetch_multiplier=1,
    worker_concurrency=16,
    worker_enable_remote_control=False,  # need this to reduce connections
    result_backend='redis://localhost:%s' %(json.loads(os.environ['DB_SERVER'])['port']),
    # result_backend='redis://:dmkTkW9Y6SuxHHxHeyGegnlEIQdQqLN5Yr6xu75C+Js=@batcanadapricingdev.redis.cache.windows.net:6379/0', # BAT cache
    redis_max_connections=20
)

@celery_app.task(bind=True, time_limit=7200, queue='pricing_queue')
def long_running_simulation_celery(self, **kwargs):

    #  update state to progress and give a status message
    self.update_state(state='PROGRESS', meta={'status': 'WORKING'})

    df_historic = pd.DataFrame(kwargs.get('df_historic'))
    df_consolidated = pd.DataFrame(kwargs.get('df_consolidated'))
    df_benchmarking_preds = pd.DataFrame(kwargs.get('df_benchmarking_preds'))
    df_pricing_input = pd.DataFrame(kwargs.get('df_pricing_input'))
    df_features = pd.DataFrame(kwargs.get('df_features'))
    df_xvar = pd.DataFrame(kwargs.get('df_xvar'))
    df_competitor_rank = pd.DataFrame(kwargs.get('df_competitor_rank'))
    df_model_endpoints = pd.DataFrame(kwargs.get('df_model_endpoints'))
    overridden_xvars_dict = {k:pd.DataFrame(kwargs.get('overridden_xvars_dict')[k]) for k in kwargs.get('overridden_xvars_dict').keys()}
    df_variable_type = (kwargs.get('df_variable_type'))
    df_switching = pd.DataFrame(kwargs.get('df_switching'))
    model_endpoints_dict = kwargs.get('model_endpoints_dict')
    model_picklefile_dict = kwargs.get('model_picklefile_dict')
    mapping_dict = kwargs.get('mapping_dict')
    period_type = kwargs.get('period_type')
    month_to_weeks = kwargs.get('month_to_weeks')
    pickle_flag = kwargs.get('pickle_flag')

    for arg in kwargs.keys():
        logger.info('%s type: %s' %(str(arg), str(type(kwargs.get(arg)))))
        if isinstance(arg, str) and arg.startswith('df'):
            logger.info('%s length: %s' %(str(arg), str(len(pd.DataFrame(kwargs.get(arg))))))

    # Initiating empty dataframe with similar no of columns as input pricing
    df_predicted = pd.DataFrame(columns=df_pricing_input.columns).drop(labels=['PRICE_PER_ITEM'], axis=1)
    
    logger.info('Raw Predictions Started')
    # Iterate via each row of Datatable 
    for row in df_pricing_input.itertuples(index=False, name='Pandas'):
        dummy_df = pd.DataFrame(columns=df_pricing_input.columns).drop(labels=['PRICE_PER_ITEM'], axis=1)
        try:
            logger.info('Generating Prediction Model for Parent Category: %s, Product Category: %s and Product: %s and sold from Shop: %s' %(row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP))
            print('Generating Prediction Model for Parent Category: %s, Product Category: %s and Product: %s and sold from Shop: %s' %(row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP))
            predict_model_instance = PredictSalesModel(row_info_data=[list(df_pricing_input.columns), row],
                                                    historic_df=df_historic,
                                                    consolidated_df=df_consolidated,
                                                    pricing_df=df_pricing_input,
                                                    features_df=df_features,
                                                    xvar_df=df_xvar,
                                                    comp_rank_df=df_competitor_rank,
                                                    overridden_xvars_dict=overridden_xvars_dict,
                                                    variable_type_df=df_variable_type,
                                                    model_endpoints_df=df_model_endpoints,
                                                    model_endpoints_dict=model_endpoints_dict,
                                                    model_picklefile_dict=model_picklefile_dict,
                                                    mapping_dict=mapping_dict,
                                                    product_info_dict={'PARENT': row.PARENT_CATEGORY, 'CATEGORY': row.PRODUCT_CATEGORY, 'PRODUCT': row.PRODUCT, 'SHOP':row.SHOP},
                                                    month_to_weeks=month_to_weeks,
                                                    pickle_flag=pickle_flag,
                                                    logger=logger)
            predict_model_instance.input_data_build(period_type=period_type)
            status_code, predicted_data = predict_model_instance.predict()
            if status_code==200:
                dummy_df = compile_prediction(period_type=period_type, 
                                            predicted_data=predicted_data, 
                                            result_df=dummy_df,
                                            row_data=row, 
                                            column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                            month2weeks=month_to_weeks,
                                            take_log=False,
                                            error=False)
            else:
                dummy_df = compile_prediction(period_type=period_type, 
                                            predicted_data=predicted_data,
                                            result_df=dummy_df, 
                                            row_data=row, 
                                            column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                            month2weeks=month_to_weeks,
                                            take_log=False,
                                            error=True)
            df_predicted = pd.concat([df_predicted, dummy_df], ignore_index = True)
        except Exception as ex:
            dummy_df = compile_prediction(period_type=period_type, 
                                        predicted_data=predicted_data, 
                                        result_df=dummy_df,
                                        row_data=row, 
                                        column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                        month2weeks=month_to_weeks,
                                        take_log=False,
                                        error=True)
            df_predicted = pd.concat([df_predicted, dummy_df], ignore_index = True)
            continue
    logger.info('Raw Predictions Ended')

    # Rounding Off the Predictions to 4 places
    df_predicted = df_predicted.round(4)

    # Replace all negative values with zero
    num = df_predicted._get_numeric_data()
    num[num < 0] = 0

    '''
    COMMENTING OUT FOR CURRENT PROBLEM STATEMENT: Since there are not too many business logics which we are inetgrating with inferencing pipeline

    # Replace zero values by moving average of last 4 weeks
    logger.info('Replacing Zeros by moving average value Started')
    df_predicted = compile_moving_average(period_type=period_type,
                                        prediction_output_df=df_predicted, 
                                        latest_sales_df=df_historic,
                                        month2weeks=month_to_weeks
                                    )
    logger.info('Replacing Zeros by moving average value Ended')
    
    # Benchmarking Predictions and Applying Thresholds
    logger.info('Benchmarking Predictions Started')
    df_predicted = custom_benchmarking(
                        prediction_output_df=df_predicted,
                        benchmarking_pred_df=df_benchmarking_preds,
                        latest_sales_df=df_historic,
                        pricing_input_df=df_pricing_input,
                        period_type=period_type,
                        start_col_index=4,
                        logger=logger
                    )
    logger.info('Benchmarking Predictions Ended')

    # Switching Logic
    logger.info('Switching Logic Implementation on Predictions Started')
    df_predicted = custom_switching(
                        prediction_output_df=df_predicted,
                        pricing_input_df=df_pricing_input,
                        latest_sales_df=df_historic,
                        switching_df=df_switching,
                        start_col_index=4,
                        logger=logger
                    )
    logger.info('Switching Logic Implementation on Predictions Ended')
    '''

    # Applying Custom Prediction Formatter
    logger.info('Custom Predictions Fornatter Started')
    df_predicted = custom_formatter(
                        prediction_output_df=df_predicted,
                        start_col_index=3,
                        before_decimal_approximation=4,
                        make_exponential=False,
                        logger=logger
                    )
    logger.info('Custom Predictions Fornatter Ended')
    
    return {'result': 'COMPLETE',
            'predicted_df': df_predicted.to_json()}

def long_running_simulation(**kwargs):
    df_historic = kwargs.get('df_historic')
    df_consolidated = kwargs.get('df_consolidated')
    df_benchmarking_preds = kwargs.get('df_benchmarking_preds')
    df_pricing_input = kwargs.get('df_pricing_input')
    df_features = kwargs.get('df_features')
    df_xvar = kwargs.get('df_xvar')
    df_competitor_rank = kwargs.get('df_competitor_rank')
    df_model_endpoints = kwargs.get('df_model_endpoints')
    overridden_xvars_dict = kwargs.get('overridden_xvars_dict')
    df_variable_type = kwargs.get('df_variable_type')
    df_switching = kwargs.get('df_switching')
    model_endpoints_dict = kwargs.get('model_endpoints_dict')
    model_picklefile_dict = kwargs.get('model_picklefile_dict')
    mapping_dict = kwargs.get('mapping_dict')
    period_type = kwargs.get('period_type')
    month_to_weeks = kwargs.get('month_to_weeks')
    pickle_flag = kwargs.get('pickle_flag')
    logger = kwargs.get('logger')
    
    # Initiating empty dataframe with similar no of columns as input pricing
    df_predicted = pd.DataFrame(columns=df_pricing_input.columns).drop(labels=['PRICE_PER_ITEM'], axis=1)
    
    logger.info('Raw Predictions Started')
    # Iterate via each row of Datatable 
    for row in df_pricing_input.itertuples(index=False, name='Pandas'):
        dummy_df = pd.DataFrame(columns=df_pricing_input.columns).drop(labels=['PRICE_PER_ITEM'], axis=1)
        try:
            logger.info('Generating Prediction Model for Parent Category: %s, Product Category: %s and Product: %s and sold from Shop: %s' %(row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP))
            print('Generating Prediction Model for Parent Category: %s, Product Category: %s and Product: %s and sold from Shop: %s' %(row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP))
            predict_model_instance = PredictSalesModel(row_info_data=[list(df_pricing_input.columns), row],
                                                    historic_df=df_historic,
                                                    consolidated_df=df_consolidated,
                                                    pricing_df=df_pricing_input,
                                                    features_df=df_features,
                                                    xvar_df=df_xvar,
                                                    comp_rank_df=df_competitor_rank,
                                                    overridden_xvars_dict=overridden_xvars_dict,
                                                    variable_type_df=df_variable_type,
                                                    model_endpoints_df=df_model_endpoints,
                                                    model_endpoints_dict=model_endpoints_dict,
                                                    model_picklefile_dict=model_picklefile_dict,
                                                    mapping_dict=mapping_dict,
                                                    product_info_dict={'PARENT': row.PARENT_CATEGORY, 'CATEGORY': row.PRODUCT_CATEGORY, 'PRODUCT': row.PRODUCT, 'SHOP':row.SHOP},
                                                    month_to_weeks=month_to_weeks,
                                                    pickle_flag=pickle_flag,
                                                    logger=logger)
            predict_model_instance.input_data_build(period_type=period_type)
            status_code, predicted_data = predict_model_instance.predict()
            if status_code==200:
                dummy_df = compile_prediction(period_type=period_type, 
                                            predicted_data=predicted_data, 
                                            result_df=dummy_df,
                                            row_data=row, 
                                            column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                            month2weeks=month_to_weeks,
                                            take_log=False,
                                            error=False)
            else:
                dummy_df = compile_prediction(period_type=period_type, 
                                            predicted_data=predicted_data,
                                            result_df=dummy_df, 
                                            row_data=row, 
                                            column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                            month2weeks=month_to_weeks,
                                            take_log=False,
                                            error=True)
            df_predicted = pd.concat([df_predicted, dummy_df], ignore_index = True)
        except Exception as ex:
            dummy_df = compile_prediction(period_type=period_type, 
                                        predicted_data=predicted_data, 
                                        result_df=dummy_df,
                                        row_data=row, 
                                        column_name_list=[row.PARENT_CATEGORY, row.PRODUCT_CATEGORY, row.PRODUCT, row.SHOP],
                                        month2weeks=month_to_weeks,
                                        take_log=False,
                                        error=True)
            df_predicted = pd.concat([df_predicted, dummy_df], ignore_index = True)
            continue
    logger.info('Raw Predictions Ended')

    # Rounding Off the Predictions to 4 places
    df_predicted = df_predicted.round(4)

    # Replace all negative values with zero
    num = df_predicted._get_numeric_data()
    num[num < 0] = 0

    '''
    COMMENTING OUT FOR CURRENT PROBLEM STATEMENT: Since there are not too many business logics which we are inetgrating with inferencing pipeline

    # Replace zero values by moving average of last 4 weeks
    logger.info('Replacing Zeros by moving average value Started')
    df_predicted = compile_moving_average(period_type=period_type,
                                        prediction_output_df=df_predicted, 
                                        latest_sales_df=df_historic,
                                        month2weeks=month_to_weeks
                                    )
    logger.info('Replacing Zeros by moving average value Ended')
    
    # Benchmarking Predictions and Applying Thresholds
    logger.info('Benchmarking Predictions Started')
    df_predicted = custom_benchmarking(
                        prediction_output_df=df_predicted,
                        benchmarking_pred_df=df_benchmarking_preds,
                        latest_sales_df=df_historic,
                        pricing_input_df=df_pricing_input,
                        period_type=period_type,
                        start_col_index=4,
                        logger=logger
                    )
    logger.info('Benchmarking Predictions Ended')

    # Switching Logic
    logger.info('Switching Logic Implementation on Predictions Started')
    df_predicted = custom_switching(
                        prediction_output_df=df_predicted,
                        pricing_input_df=df_pricing_input,
                        latest_sales_df=df_historic,
                        switching_df=df_switching,
                        start_col_index=4,
                        logger=logger
                    )
    logger.info('Switching Logic Implementation on Predictions Ended')
    '''

    # Applying Custom Prediction Formatter
    logger.info('Custom Predictions Fornatter Started')
    df_predicted = custom_formatter(
                        prediction_output_df=df_predicted,
                        start_col_index=3,
                        before_decimal_approximation=4,
                        make_exponential=False,
                        logger=logger
                    )
    logger.info('Custom Predictions Fornatter Ended')
    
    return df_predicted