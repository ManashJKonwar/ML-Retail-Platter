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
from dash.dependencies import Input, Output, State, MATCH
from callback_manager import CallbackManager
from layouts.layout_kpis import get_kpi_widget_template
from datasets.backend import shop_names, df_transactions_weekly
from utility.utility_kpi import KPICalculation

callback_manager = CallbackManager()

# Adding Dynamic KPI Child Widget
@callback_manager.callback(Output(component_id='kpi-widget-container', component_property='children'),
                        Input(component_id='add-kpi-widgets', component_property='n_clicks'),
                        State(component_id='kpi-widget-container', component_property='children'))
def display_graphs(n_clicks, div_children):
    if n_clicks is not None:
        new_child = get_kpi_widget_template(n_clicks=n_clicks)
        div_children.append(new_child)
    return div_children

# Setting up dropdown value for Dynamic Channel Dropdown
@callback_manager.callback([Output(component_id={'type':'dynamic-dd-shop', 'index': MATCH}, component_property='options'),
                        Output(component_id={'type':'dynamic-dd-shop', 'index': MATCH}, component_property='value')],
                        Input(component_id='dd-shop-name', component_property='value'))
def set_channel_parameters(shop_list):
    # Extract Selected Shops 
    shop_selected_list = []
    try:
        if isinstance(shop_list, list) and len(shop_list)>0:
            for selected_shop in shop_list:
                shop_selected_list.append(selected_shop)
        else:
            shop_selected_list = copy.deepcopy(shop_names)
    except Exception:
        pass
    options = [{'label': i, 'value': i} for i in shop_selected_list]
    return options, shop_selected_list

# Setting up KPI Parameters and Graphical Representation
@callback_manager.callback([Output(component_id={'type': 'dynamic-graph', 'index': MATCH}, component_property='figure'),
                        Output(component_id={'type': 'dynamic-historic-value', 'index': MATCH}, component_property='children'),
                        Output(component_id={'type': 'dynamic-predicted-value', 'index': MATCH}, component_property='children'),
                        Output(component_id={'type': 'dynamic-change-value', 'index': MATCH}, component_property='children'),
                        Output(component_id={'type': 'dynamic-change-value', 'index': MATCH}, component_property='style'),
                        Output(component_id={'type': 'dynamic-dd-shop', 'index': MATCH}, component_property='style')],
                        [Input(component_id={'type': 'dynamic-dd-shop', 'index': MATCH}, component_property='value'),
                        Input(component_id={'type': 'dynamic-dd-kpi', 'index': MATCH}, component_property='value'),
                        Input(component_id={'type': 'dynamic-choice', 'index': MATCH}, component_property='value')],
                        [State(component_id='dd-shop-name', component_property='value'),
                        State(component_id='dd-period', component_property='value'),
                        State(component_id='storage-pricing-input', component_property='data'),
                        State(component_id='storage-pricing-output', component_property='data')])
def update_graph(shop_value_list, kpi_value, chart_choice, shop_type, period_type, pricing_input_data, predicted_sales_data):

    df_weekly_sales_transactions = df_transactions_weekly.copy()

    current_value, predicted_value, change, change_color, fig = 0.0, 0.0, 0.0, None, None
    if kpi_value.__eq__('Product Volume'):
        kpi_calculator = KPICalculation(
                            calculation_parameter=kpi_value,
                            granularity=period_type,
                            fig_type=chart_choice,
                            df_product_historic=df_weekly_sales_transactions,
                            df_product_pricing=pd.DataFrame(pricing_input_data),
                            df_product_prediction=pd.DataFrame(predicted_sales_data)
                        )
        kpi_calculator._kpi_instance.calculate()