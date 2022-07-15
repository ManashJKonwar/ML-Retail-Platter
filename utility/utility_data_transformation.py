__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import ast
import math
import numpy as np
import pandas as pd
import datetime as dt
import calendar as ca
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

SYMBOL_REMOVAL=['"','[',']','{','}','predict',':']

#region Date Related Data Transformations
# Long term monthly window structure
def long_term_structure():
    """
    Extracts 52 weeks/12 months data in both weekly format as well as monthly format
    """
    ltcurrentmonth = date.today().replace(day=1) #first day of the month
    ltnextyear = ltcurrentmonth+relativedelta(months=12) #change here for the month range
    ltmonthrange = []
    while ltcurrentmonth < ltnextyear: #for normal monthframe used
        ltcurrentmonth = ltcurrentmonth+relativedelta(months=1)
        ltmonthrange.append(str(ltcurrentmonth.year)+"-"+str(ltcurrentmonth.strftime("%b"))+"-"+str(ltcurrentmonth.strftime("%d"))) #form of YYYY-MM-DD

    # Long term weekly window structure
    ltcurrentmonth_forweek = date.today().replace(day=1) #first day of the month
    ltnextyear_forweek = ltcurrentmonth_forweek+relativedelta(months=13) #change here for the month range +1
    ltmonthrange_forweek = []
    while ltcurrentmonth_forweek < ltnextyear_forweek: #for generating week range
        ltcurrentmonth_forweek = ltcurrentmonth_forweek+relativedelta(months=1)
        ltmonthrange_forweek.append(str(ltcurrentmonth_forweek.year)+"-"+str(ltcurrentmonth_forweek.strftime("%b"))+"-"+str(ltcurrentmonth_forweek.strftime("%d"))) #form of YYYY-MM-DD

    # Generating weekly window structure
    ltmin_month = ltmonthrange_forweek[0]
    ltmax_month = ltmonthrange_forweek[-1]
    ltweek_from_month_base = pd.date_range(start=ltmin_month, end=ltmax_month, freq="W-MON") #generate week range based on month range
    ltweek_from_month = pd.DataFrame(data=ltweek_from_month_base)
    ltweek_from_month.columns = ["dt_sales"]
    ltweek_from_month["dt_sales"] = ltweek_from_month["dt_sales"].astype("datetime64[ns]")
    ltweek_from_month["year"] = ltweek_from_month["dt_sales"].dt.year
    ltweek_from_month["month"] = ltweek_from_month["dt_sales"].dt.month
    ltweek_from_month["week"] = ltweek_from_month["dt_sales"].dt.isocalendar().week
    ltweek_from_month["year"] = ltweek_from_month["year"].astype("int64")
    ltweek_from_month["month"] = ltweek_from_month["month"].astype("int64")
    ltweek_from_month["week"] = ltweek_from_month["week"].astype("int64")

    # For input structure
    ltmonthtoweeklist = [i.strftime("%Y-%b-%d") for i in ltweek_from_month["dt_sales"]]

    return ltmonthrange, ltmonthtoweeklist

# Short term weekly window structure
def short_term_structure():
    """
    Extracts 13 weeks/3 months data in both weekly format as well as monthly format
    """
    stcurrentmonth = date.today().replace(day=1) #first day of the month
    stnextyear = stcurrentmonth+relativedelta(weeks=13) #change here for the month range
    stmonthrange = []
    while stcurrentmonth < stnextyear: #for normal monthframe used
        stcurrentmonth = stcurrentmonth+relativedelta(months=1)
        stmonthrange.append(str(stcurrentmonth.year)+"-"+str(stcurrentmonth.strftime("%b"))+"-"+str(stcurrentmonth.strftime("%d"))) #form of YYYY-MM-DD

    # Short term weekly window structure
    stcurrentmonth_forweek = date.today().replace(day=1) #first day of the month
    stnextyear_forweek = stcurrentmonth_forweek+relativedelta(weeks=14) #change here for the month range +1
    stmonthrange_forweek = []
    while stcurrentmonth_forweek < stnextyear_forweek: #for generating week range
        stcurrentmonth_forweek = stcurrentmonth_forweek+relativedelta(months=1)
        stmonthrange_forweek.append(str(stcurrentmonth_forweek.year)+"-"+str(stcurrentmonth_forweek.strftime("%b"))+"-"+str(stcurrentmonth_forweek.strftime("%d"))) #form of YYYY-MM-DD

    # Generating weekly window structure
    stmin_month = stmonthrange_forweek[0]
    stmax_month = stmonthrange_forweek[-1]
    stweek_from_month_base = pd.date_range(start=stmin_month, end=stmax_month, freq="W-MON") #generate week range based on month range
    stweek_from_month = pd.DataFrame(data=stweek_from_month_base[0:-1])
    stweek_from_month.columns = ["dt_sales"]
    stweek_from_month["dt_sales"] = stweek_from_month["dt_sales"].astype("datetime64[ns]")
    stweek_from_month["year"] = stweek_from_month["dt_sales"].dt.year
    stweek_from_month["month"] = stweek_from_month["dt_sales"].dt.month
    stweek_from_month["week"] = stweek_from_month["dt_sales"].dt.isocalendar().week
    stweek_from_month["year"] = stweek_from_month["year"].astype("int64")
    stweek_from_month["month"] = stweek_from_month["month"].astype("int64")
    stweek_from_month["week"] = stweek_from_month["week"].astype("int64")

    # For input structure
    stmonthtoweeklist = [i.strftime("%Y-%b-%d") for i in stweek_from_month["dt_sales"]]

    return stmonthrange, stmonthtoweeklist

# Next month start and end dates
def get_custom_dates():
    """
    Extracts the first start date of next month and also the last date of the next month
    """
    today = date.today()
    custom_start_date = today.replace(day=1) + relativedelta(months=1)
    custom_end_date = today.replace(day=1) + relativedelta(months=2) - timedelta(days=1)
    return custom_start_date, custom_end_date

# Extract custom dates ar weekly level
def custom_datepicker(start_date=None, end_date=None):
    """
    This method extracts month list and week list between a custom
    start date and end date
    Parameters: 
        start_date (str): custom start date
        end_date (str): custom_end_date
    Returns: 
        month_list (list, str): List collection of months falling exclusively within
                            custom dates
        week_list (list, str): List collection of weeks falling exclusively within
                            custom dates
    """
    if start_date is not None and end_date is not None:
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
        week_list, month_dict=[],{}
        for i in range((end_date - start_date).days):
            day = ca.day_name[(start_date + dt.timedelta(days=i+1)).weekday()]
            if day.__eq__('Monday') and (start_date + dt.timedelta(days=i+1)).weekday() not in week_list:
                week_list.append(start_date + dt.timedelta(days=i+1))

        for date in week_list:
            if (dt.datetime(date.year,date.month,1)) in month_dict.keys():
                month_dict[dt.datetime(date.year,date.month,1)].append(date)
            else:
                month_dict[dt.datetime(date.year,date.month,1)] = [date]

        # For input structure, Converting week list to specific format
        week_list_input = [i.strftime("%Y-%b-%d") for i in week_list]
        # month_list_input=[month.split('-')[2]+'-'+ for month in month_dict.keys()]
        month_list_input = [i.strftime("%Y-%b-%d") for i in month_dict.keys()]

        return month_list_input, week_list_input
#endregion

#region Prediction Compiler
def compile_prediction(**kwargs):
    """
    This method compiles prediciton output based on 3 types of granularity:
    1. Weekly
    2. Annually i.e. Monthly
    3. Custom expressed as extension of Weekly
    Parameters: 
        kwargs : Multiple Arguments
            period_type (str): type of granularity (options are weekly, annually and custom)
            predicted_data (str): string response from model service
            result_df (pandas dataframe): Dataframe Framework to fill in details
            row_data (pandas series): provides information on some extra colums 
            column_name_list (list, str): list of column names to iterate on
            month2weeks (list, str): List of all available weeks within simualtion period i.e.  Monday of each week
            take_log (bool): If log needs to be taken or not based on type of model
            error (bool): if its an error predicted data or successful one
    Returns: 
        result_df (pandas dataframe): Dataframe Framework Aggregated Properly with prediction
    """
    period_type = kwargs.get('period_type')
    predicted_data = kwargs.get('predicted_data')
    result_df = kwargs.get('result_df')
    row_data = kwargs.get('row_data')
    column_name_list = kwargs.get('column_name_list')
    month2weeks = kwargs.get('month2weeks')
    take_log = kwargs.get('take_log')
    error = kwargs.get('error')
    if not error:
        # Cleaning Predicted Message
        for item in SYMBOL_REMOVAL:
            predicted_data = predicted_data.replace(item,'')
        result = ast.literal_eval(predicted_data.strip())
        # Check if models used are log-linear models
        if take_log:
            result = tuple([np.expm1(item) for item in result])
            if any(math.isinf(prediction) for prediction in result):
                modified_result = []
                for prediction in result:
                    modified_result.append(0.0) if math.isinf(prediction) else modified_result.append(prediction)
                result = tuple(modified_result)

        if period_type.__eq__('Quarterly') or period_type.__eq__('Custom'):
            if isinstance(result, tuple):
                result_df.loc[0] = column_name_list+list(result)
                return result_df
        elif period_type.__eq__('Annually'):
            if isinstance(result, tuple):
                # Perform Avg Aggregation for converting weekly level predictions
                # to month level data
                month_map, month_agg={},{}
                predicted_list, extraction_counter = list(result), 0
                iterative_list = list(result_df.columns[3:]) 
                for item in iterative_list:
                    try:
                        item_year_month = '-'.join(item.split('-')[0:2])
                        month_map[item_year_month] = [x for x in month2weeks if '-'.join(x.split('-')[0:2]) == item_year_month]
                        if len(month_map[item_year_month])>0:
                            agg_predicted_list = predicted_list[extraction_counter:(extraction_counter+len(month_map[item_year_month]))]
                            month_agg[item] = round(sum(agg_predicted_list),2)
                            extraction_counter+=len(month_map[item_year_month])
                    except Exception:
                        month_agg[item] = 'Aggregation Error'
                        continue
                result_df.loc[0] = column_name_list+list(month_agg.values())
                return result_df
    else:
        if isinstance(predicted_data, str):
            result_df.loc[0] = [row_data.PROVINCE, row_data.MANUF, row_data.BRAND]+[predicted_data for i in range(len(result_df.columns)-3)]
            return result_df
#endregion

#region Custom Formatter
def custom_formatter(**kwargs):
    """
    This method is utilize to convert each prediction per brand into a customized string format
    Parameters: 
        kwargs : Multiple Arguments
            prediction_output_df (pandas dataframe): predicted dataframe in same order as that of pricing input
            start_col_index (int): Data Column Starting Index in Prediction Output
            before_decimal_approximation (int): How many decimals to round up if predictions are to be expressed in 
                                                exponential form
            make_exponential (bool): True or False (by default False)
            logger (logging object): Logger
    Returns: 
        modified_prediction_df (pandas dataframe): predicted dataframe in with string formatted data
                                                e.g. by default the predictions are represented as exponential form
                                                with a limitation of how many digits needs to be present before decimal
    """
    prediction_output_df = kwargs.get('prediction_output_df')
    start_col_index = kwargs.get('start_col_index')
    before_decimal_approximation = kwargs.get('before_decimal_approximation')
    make_exponential = kwargs.get('make_exponential') if 'make_exponential' in kwargs.keys() else False
    logger = kwargs.get('logger')
    
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def format_predictions(row_data=None,
                           start_col_index=start_col_index,
                           before_decimal_approximation=before_decimal_approximation):
        formatted_col_dict = {}
        try:
            predictions = [row_data[predicted_date] for predicted_date in list(row_data[start_col_index:].index)]
            n = before_decimal_approximation
            col_counter = 0
            for prediction in predictions:
                modified_prediction = None 
                current_predicition = prediction               
                if isfloat(current_predicition):
                    if make_exponential:
                        e = math.ceil(math.log10(current_predicition) - n)
                        n_digits = current_predicition * 10**-e
                        if e:
                            modified_prediction = '%.0fe%d' % (n_digits, e)
                        else:
                            modified_prediction = '%.0f' % (current_predicition)
                    else:
                        modified_prediction = round(current_predicition,0)
                else:
                    modified_prediction = prediction

                if row_data[start_col_index:].index[col_counter] not in formatted_col_dict.keys():
                    formatted_col_dict[row_data[start_col_index:].index[col_counter]] = modified_prediction
                
                col_counter+=1
        except Exception: 
            pass
        finally:
            return formatted_col_dict

    modified_prediction_df=prediction_output_df.copy()
    if prediction_output_df is not None:
        for row_Index, row_Data in prediction_output_df.iterrows():
            try:
                formatted_col_dict = format_predictions(row_data=row_Data)
                for colname in prediction_output_df.columns[start_col_index:]:
                    modified_prediction_df.iloc[row_Index, prediction_output_df.columns.get_loc(colname)] = formatted_col_dict[colname]
                logger.info('Custom Formatting Done Successfully for Product Category: %s, Product: %s and Shop: %s' %(str(row_Data.PRODUCT_CATEGORY), str(row_Data.PRODUCT), str(row_Data.SHOP)))
            except Exception as ex:
                logger.error('Custom Formatting Caught exception for Product Category: %s, Product: %s and Shop: %s with exception as %s' %(str(row_Data.PRODUCT_CATEGORY), str(row_Data.PRODUCT), str(row_Data.SHOP), str(ex)))
                continue
        return modified_prediction_df  
    else:
        return prediction_output_df.copy()
#endregion