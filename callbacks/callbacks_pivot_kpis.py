__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts.layout_pivot_kpis import get_pivot_table_children

callback_manager = CallbackManager()

# Updating Pivot Table Data
@callback_manager.callback([Output(component_id='pivot-table', component_property='data'),
                        Output(component_id='pivot-table', component_property='rowOrder'),
                        Output(component_id='pivot-table', component_property='colOrder')],
                        Input(component_id='storage-pricing-output', component_property='data'),
                        State(component_id='storage-pricing-input', component_property='data'))
def update_pivot_table(stored_sales_prediction, stored_pricing_data):
    if stored_sales_prediction is not None:
        error=False
        try:
            df_predicted = pd.DataFrame(stored_sales_prediction)
            df_pricing = pd.DataFrame(stored_pricing_data)
            # Breakdown Pricing to week level information
            df_pricing = pd.melt(df_pricing, id_vars=['PRODUCT_CATEGORY','PRODUCT','SHOP'], value_vars=list(df_pricing.columns[4:]), var_name='WEEK_DATE', value_name='SIMULATED_PRICING')
            # Breakdown Predictions to week level information
            df_predicted = pd.melt(df_predicted, id_vars=['PRODUCT_CATEGORY','PRODUCT','SHOP'], value_vars=list(df_predicted.columns[3:]), var_name='WEEK_DATE', value_name='SALES_VOLUME')
            # Merge Pricing to Predicted Data
            df_predicted = pd.merge(df_predicted, df_pricing, on=['PRODUCT_CATEGORY','PRODUCT','SHOP','WEEK_DATE'])
            # Adition of Sales Revenue after casting 
            df_predicted['SIMULATED_PRICING'] = df_predicted['SIMULATED_PRICING'].astype(float)
            df_predicted['SALES_REVENUE'] = df_predicted['SALES_VOLUME'] * df_predicted['SIMULATED_PRICING']
            # Get Quarterly Representation of the year
            df_predicted['QUARTERLY_REPRESENTATION'] = pd.PeriodIndex(pd.to_datetime(df_predicted['WEEK_DATE']), freq='Q').astype(str)
            # Get Yearly Representation
            df_predicted['YEARLY_REPRESENTATION'] = pd.to_datetime(df_predicted['WEEK_DATE']).dt.year.astype(str)
            # Convert Predicted Data to list of list for each row including the column header naming list as well
            data = [list(df_predicted.columns)]+df_predicted.values.tolist()
            # Populating Pivot table parameters
            row_order, col_order= None, None
            if len(data)>1:
                row_order='key_a_to_z'
                col_order='key_a_to_z'
        except Exception:
            error=True
        finally:
            if error:
                return dash.no_update, dash.no_update, dash.no_update
            else:
                return data, row_order, col_order
    else:   
        return dash.no_update, dash.no_update, dash.no_update

# Displaying Pivot Table Components based on Pivot Table Parameters Selection
@callback_manager.callback(Output(component_id='pivotting-output', component_property='children'),
                        [Input(component_id='pivot-table', component_property='cols'),
                        Input(component_id='pivot-table', component_property='rows'),
                        Input(component_id='pivot-table', component_property='rowOrder'),
                        Input(component_id='pivot-table', component_property='colOrder'),
                        Input(component_id='pivot-table', component_property='aggregatorName'),
                        Input(component_id='pivot-table', component_property='rendererName')])
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    pivot_children_list = get_pivot_table_children(
                                            cols=cols,
                                            rows=rows,
                                            row_order=row_order,
                                            col_order=col_order,
                                            aggregator=aggregator,
                                            renderer=renderer
                                        )
    return pivot_children_list