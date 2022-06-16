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
from layouts import layout_retail_summary

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='tabs-content', component_property='children'),
                        Input(component_id='tabs', component_property='value'))
def render_content(tab):
    if tab == 'tab-1':
        return layout_retail_summary.layout