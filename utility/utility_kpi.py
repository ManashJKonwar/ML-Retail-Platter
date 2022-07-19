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

        if self._kpi_calculation.granularity.__eq__('Custom') or self._kpi_calculation.granularity.__eq__('Quarterly'):
            print('here')
        else:
            print('here')