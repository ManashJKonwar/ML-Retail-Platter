__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from dash.dependencies import Input, Output
from layouts.layout_authentication import create, login, success, failed, data, logout
from callback_manager import CallbackManager

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='auth-page-content', component_property='children'),
                        Input(component_id='auth-url', component_property='pathname'))
def display_page(pathname):
    if pathname == '/':
        return create
    elif pathname == '/login':
        return login
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success
        else:
            return failed
    elif pathname =='/data':
        if current_user.is_authenticated:
            return data
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    else:
        return '404'