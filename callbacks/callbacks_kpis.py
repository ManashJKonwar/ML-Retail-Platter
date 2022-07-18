__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import copy
from dash.dependencies import Input, Output, State, MATCH
from callback_manager import CallbackManager
from layouts.layout_kpis import get_kpi_widget_template
from datasets.backend import shop_names

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