__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from dash import dcc
from dash import html
from dash import no_update
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts.layout_authentication import create, login, success, failed, data, logout
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc as sqlalchemy_exc

callback_manager = CallbackManager()

# conn = sqlite3.connect('data.sqlite')
# engine = create_engine('sqlite:///data.sqlite')
# Users_tbl = Table('users', Users.metadata)

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

# Callback related to "Create User" Section
@callback_manager.callback(Output(component_id='container-button-basic', component_property="children"),
                        Input(component_id='btn-submit-user', component_property='n_clicks'),
                        [State(component_id='text-username', component_property='value'), 
                        State(component_id='text-password', component_property='value'), 
                        State(component_id='text-email', component_property='value')], prevent_initial_call=True)
def insert_users(n_clicks, un, pw, em):
    if un is not None and pw is not None and em is not None:
        from app import engine, users_tbl
        hashed_password = generate_password_hash(pw, method='sha256')
        ins = users_tbl.insert().values(username=un,  password=hashed_password, email=em,)
        conn = engine.connect()
        try:
            conn.execute(ins)
        except sqlalchemy_exc.SQLAlchemyError as ex:
            if 'sqlite3.OperationalError' in ex.args[0] and 'no such table' in ex.args[0]:
                try:
                    print("Creating a new table: ")
                    conn.execute('''
                        CREATE TABLE users(
                        id integer primary_key, 
                        username text unique, 
                        email text, 
                        password text
                    )''')
                    print("New table created successfully!!!")
        
                    conn.execute(ins)
                except sqlite3.Error() as e:
                    print(e, " occured")
        conn.close()
        return [login]
    elif un is None and pw is None and em is None:
        return no_update
    else:
        return [html.Div([html.H2('Already have a user account?'), dcc.Link('Click here to Log In', href='/login')])]

# Callback related to "Login User" Section
@callback_manager.callback(Output(component_id='url_login', component_property='pathname'),
                        Input(component_id='btn-login', component_property='n_clicks'),
                        [State(component_id='text-uname-box', component_property='value'), 
                        State(component_id='text-pwd-box', component_property='value')])
def successful(n_clicks, ip_uname, ip_pass):
    from app import User
    user = User.query.filter_by(username=ip_uname).first()
    if user:
        if check_password_hash(user.password, ip_pass):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass