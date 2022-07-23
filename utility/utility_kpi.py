__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
from utility.utility_visualizations import Bar, Line, Pie

class KPICalculation():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._current_value = 0.0
        self._predicted_value = 0.0
        self._change = 0.0
        self._change_color_label = '#E0E0E0'
        self._kpi_instance = self.set_kpi()
        self._fig_instance = self.set_fig()
        self._fig_data = {
                            'current':{
                                'x-data':[],
                                'y-data':[]
                                },
                            'predicted':{
                                'x-data':[],
                                'y-data':[]
                            }
                        }

    def set_kpi(self):
        if self.calculation_parameter.__eq__('Product Volume'):
            return ProductVolume(self)
        elif self.calculation_parameter.__eq__('Product Profit'):
            return ProductProfit(self)
        elif self.calculation_parameter.__eq__('SOP'):
            return SOP(self)

    def set_fig(self):
        if self.fig_type.__eq__('bar'):
            return Bar(title=self.calculation_parameter, data=None)
        elif self.fig_type.__eq__('line'):
            return Line(title=self.calculation_parameter, data=None)
        elif self.fig_type.__eq__('pie'):
            return Pie(title=self.calculation_parameter, data=None)

    def get_kpi_parameters(self):
        return self._current_value, self._predicted_value, self._change, self._change_color_label

    def set_label_color(self):
        try:
            if self._change<0:
                self._change_color_label="#FF0000"
            elif self._change>0:
                self._change_color_label="#228B22"
            else:
                self._change_color_label="#E0E0E0"
        except:
            pass

class ProductVolume():
    def __init__(self, kpi_calculation):
        self._kpi_calculation = kpi_calculation

    def calculate(self):
        df_product_historic = self._kpi_calculation.__dict__.get("df_product_historic")
        df_product_pricing = self._kpi_calculation.__dict__.get("df_product_pricing")
        df_product_prediction = self._kpi_calculation.__dict__.get("df_product_prediction")

        # Filtering only selected products
        product_mask = (df_product_historic.product_category.isin(list(df_product_pricing.PRODUCT_CATEGORY.unique()))) & \
                    (df_product_historic.product_name.isin(list(df_product_pricing.PRODUCT.unique()))) & \
                    (df_product_historic.shop_name.isin(list(df_product_pricing.SHOP.unique())))
        df_product_historic = df_product_historic.loc[product_mask].reset_index(drop=True)

        # Summing all volumes
        df_product_historic = df_product_historic.groupby('week_start_date').agg({'item_cnt_day':'sum'}).reset_index()

        # Sorting dates based on week dates
        df_product_historic = df_product_historic.sort_values(by=['week_start_date'], ascending=False).reset_index(drop=True)

        if self._kpi_calculation.granularity.__eq__('Custom') or self._kpi_calculation.granularity.__eq__('Quarterly'):
            week_counter = 12 # Counter values for number of weeks to retain
            
            # Dynamically number of weeks to retain based on weekly run
            if self._kpi_calculation.granularity.__eq__('Custom'):
                week_counter = len(df_product_prediction.columns[3:])
           
            # Extracting unique week dates and getting the top 12 weeks
            weekly_dates = list(df_product_historic.week_start_date.unique())[:week_counter]

            # Retaining only relevant weeks
            df_product_historic = df_product_historic.loc[df_product_historic.week_start_date.isin(weekly_dates)]

            # Calculating Current and Projected Changes
            self._kpi_calculation._current_value = float(df_product_historic.item_cnt_day.sum())
            self._kpi_calculation._predicted_value = float(df_product_prediction[df_product_prediction.columns[3:]].sum(numeric_only=True).sum())
            self._kpi_calculation._change = ((self._kpi_calculation._predicted_value-self._kpi_calculation._current_value)/self._kpi_calculation._current_value) * 100
        
            #Set x and y data after sorting out the data
            df_current_data, df_predicted_data = None, None
            # Extract Current and Predicted dataframes
            try:
                df_current_data = df_product_historic.copy()
                df_predicted_data = df_product_prediction.copy()
            except Exception:
                pass
        else:
            week_counter = 52 # Counter values for number of weeks to retain

            # Extracting unique week dates and getting the top 12 weeks
            weekly_dates = list(df_product_historic.week_start_date.unique())[:week_counter]

            # Retaining only relevant weeks
            df_product_historic = df_product_historic.loc[df_product_historic.week_start_date.isin(weekly_dates)]

            # Calculating Current and Projected Changes
            self._kpi_calculation._current_value = float(df_product_historic.item_cnt_day.sum())
            self._kpi_calculation._predicted_value = float(df_product_prediction[df_product_prediction.columns[3:]].sum(numeric_only=True).sum())
            self._kpi_calculation._change = ((self._kpi_calculation._predicted_value-self._kpi_calculation._current_value)/self._kpi_calculation._current_value) * 100
        
            #Set x and y data after sorting out the data
            df_current_data, df_predicted_data = None, None
            # Extract Current and Predicted dataframes
            try:
                df_current_data = df_product_historic.copy()
                df_predicted_data = df_product_prediction.copy()
            except Exception:
                pass

        self._kpi_calculation._fig_data['current']['x-data']=[x.strftime("%Y-%b-%d") for x in df_current_data.week_start_date.to_list()]
        self._kpi_calculation._fig_data['current']['y-data']=df_current_data.item_cnt_day.to_list()
        self._kpi_calculation._fig_data['predicted']['x-data']=list(df_predicted_data[df_predicted_data.columns[3:]].sum(numeric_only=True).index)
        self._kpi_calculation._fig_data['predicted']['y-data']=df_predicted_data[df_predicted_data.columns[3:]].sum(numeric_only=True).to_list()

class SOP:
    def __init__(self, kpi_calculation):
        self._kpi_calculation = kpi_calculation

    def calculate(self):
        df_product_historic = self._kpi_calculation.__dict__.get("df_product_historic")
        df_product_pricing = self._kpi_calculation.__dict__.get("df_product_pricing")
        df_product_prediction = self._kpi_calculation.__dict__.get("df_product_prediction")

        # Filtering only selected products
        product_mask = (df_product_historic.product_category.isin(list(df_product_pricing.PRODUCT_CATEGORY.unique()))) & \
                    (df_product_historic.product_name.isin(list(df_product_pricing.PRODUCT.unique()))) & \
                    (df_product_historic.shop_name.isin(list(df_product_pricing.SHOP.unique())))
        df_product_historic = df_product_historic.loc[product_mask].reset_index(drop=True)

        # Sorting dates based on week dates
        df_product_historic = df_product_historic.sort_values(by=['week_start_date'], ascending=False).reset_index(drop=True)

        if self._kpi_calculation.granularity.__eq__('Custom') or self._kpi_calculation.granularity.__eq__('Quarterly'):
            week_counter = 12 # Counter values for number of weeks to retain
            
            # Dynamically number of weeks to retain based on weekly run
            if self._kpi_calculation.granularity.__eq__('Custom'):
                week_counter = len(df_product_prediction.columns[3:])
           
            # Extracting unique week dates and getting the top 12 weeks
            weekly_dates = list(df_product_historic.week_start_date.unique())[:week_counter]

            # Retaining only relevant weeks
            df_product_historic = df_product_historic.loc[df_product_historic.week_start_date.isin(weekly_dates)]

            # Adding up no of counts per category for each week dates
            df_product_historic = df_product_historic.groupby(['week_start_date','product_category']).agg({'item_cnt_day':'sum'}).reset_index()
        else:
            print('here')