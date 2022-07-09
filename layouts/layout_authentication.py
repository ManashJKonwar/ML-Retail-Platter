__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

create = html.Div([ 
            html.H1('Create User Account'), 
            dcc.Location(id='create_user', refresh=True),
            dcc.Input(
                id="text-username",
                type="text",
                placeholder="user name",
                maxLength =15),
            dcc.Input(
                id="text-password",
                type="password",
                placeholder="password"),
            dcc.Input(
                id="text-email",
                type="email",
                placeholder="email",
                maxLength = 50),
            html.Button('Create User', id='btn-submit-user', n_clicks=0),
            html.Div(id='container-button-basic')
        ])

left_login_jumbotron = dbc.Col(
                            html.Div(
                                [
                                    html.H2("Pricing Simulator", className="display-3"),
                                    html.Hr(className="my-2"),
                                    html.P(
                                        "Visualize, Simulate and Project Pricing Scenarios."
                                    ),
                                ],
                                className="h-100 p-5 text-white bg-dark rounded-3",
                            ),
                            style={'height': '100vh', 'padding': '25px'},
                            md=8,
                        )

right_login_jumbotron = dbc.Col(
                            html.Div([
                                    html.H2("Login", className="display-3"),
                                    html.Hr(className="my-2"),
                                    html.P(
                                        "Use your credentials to access the fun."
                                    ),
                                    dbc.Input(
                                        placeholder='Enter your username', 
                                        type='text',
                                        id='text-uname-box'),
                                    dbc.Input(
                                        placeholder='Enter your password', 
                                        type='password',
                                        id='text-pwd-box',
                                        style={"margin-top": "5px"}),
                                    dbc.Button(
                                        children='Login',
                                        n_clicks=0,
                                        type='submit',
                                        id='btn-login',
                                        color='primary',
                                        style={"margin-top": "5px"}),
                                    dbc.Button(
                                        children='Sign Up',
                                        n_clicks=0,
                                        type='submit',
                                        id='btn-signup',
                                        color='primary',
                                        style={"margin-top": "5px", "margin-left": "5px"}),
                                    dcc.Location(id='url_login', refresh=True),
                                    dcc.Location(id='url_create', refresh=True),
                                    html.Div(children='', id='output-state')
                                ],
                                className="h-100 p-5 bg-light border rounded-3",
                            ),
                            style={'height': '100vh', 'padding': '25px'},
                            md=4
                        ) 

login = dbc.Row(
            [left_login_jumbotron, right_login_jumbotron],
            className="align-items-md-stretch",
        )

success = html.Div([
            dcc.Location(id='url_login_success', refresh=True),
            html.Div([
                html.H2('Login successful.'),
                html.Br(),
                html.P('Select "Open Simulator" link below'),
                dcc.Link('Open Simulator', href = '/simulator')
            ]),
            html.Div([
                html.Br(),
                html.Button(id='btn-back', children='Go back', n_clicks=0)
            ]) 
        ])

data = html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in ['Day 1', 'Day 2']],
                value='Day 1'),
            html.Br(),
            html.Div([dcc.Graph(id='graph')])
        ])

failed = html.Div([ 
            dcc.Location(id='url_login_df', refresh=True),
            html.Div([
                html.H2('Log in Failed. Please try again.'),
                html.Br(),
                html.Div([login]),
                html.Br(),
                html.Button(id='btn-back', children='Go back', n_clicks=0)
            ])
        ])

logout = html.Div([
            dcc.Location(id='logout', refresh=True),
            html.Br(),
            html.Div(html.H2('You have been logged out - Please login')),
            html.Br(),
            html.Div([login]),
            html.Button(id='btn-back', children='Go back', n_clicks=0)
    ])

layout = html.Div([
            html.Div(id='auth-page-content', className='content'),
            dcc.Location(id='auth-url', refresh=False)
        ])