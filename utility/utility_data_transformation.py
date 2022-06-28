__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
import datetime as dt
import calendar as ca
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

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