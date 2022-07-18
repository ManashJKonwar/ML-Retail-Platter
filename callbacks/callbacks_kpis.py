__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts.layout_kpis import get_kpi_widget_template

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