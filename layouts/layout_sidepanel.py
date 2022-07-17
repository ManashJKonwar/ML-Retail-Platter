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
from dash_bootstrap_templates import ThemeChangerAIO

from datasets.backend import product_categories, shop_names, product_names, custom_start_date, custom_end_date
# from backend import channel_type, analysis_type, granularity, maker_type, device_family, spinner

tab_height = '7vh'
layout = dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.Div(
                        html.A(
                            html.Img(
                                id='bat-logo',
                                height='60vh'
                                )
                            ),
                        style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10, 'text-align':'center'}),
                    width=3),
                dbc.Col(
                    html.Div(
                        html.A(
                            html.H1('RETAIL PRICING SIMULATOR', style={'text-align': 'center', 'font-weight': 'bold', 'color': '#000000'})
                            ),
                        style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
                    width=8),
                dbc.Col(
                    html.Div(
                            ThemeChangerAIO(
                                aio_id="theme", 
                                radio_props={"value":dbc.themes.BOOTSTRAP}
                            ),
                        style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}), 
                    width=1)
            ], style={'backgroundColor':'#D3D3D3'},  className="h-15",),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Details([
                            html.Summary('Simulation Filter', style={'font-weight': 'bold', 'color': '#000000'}),
                            # Custom Data Selection Filter
                            html.Label('Custom Date Selection:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.DatePickerRange(
                                id='dpr-period',
                                start_date=custom_start_date,
                                end_date=custom_end_date,
                                style={
                                    'fontSize': '2vh',
                                    'color': 'black',
                                }),
                            ]),
                            # Period Filter
                            html.Label('Period Type:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-period',
                                    options=[{'label': i, 'value': i} for i in ['Quarterly','Annually','Custom']],
                                    value='Custom',
                                    searchable=False,
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                ),
                            ])
                        ],
                        id='simulation-detail',  
                        style={'color': '#000000', 'margin-top': '2vh', 'border':'1px white solid'}),
                        html.Details([
                            html.Summary('Prediction Filter', style={'font-weight': 'bold', 'color': '#000000'}),
                            # Prediction Filter
                            html.Label('Prediction Type:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.RadioItems(
                                    id='radioitem-prediction',
                                    options=[
                                        {'label': 'Item Count', 'value': 'Count'},
                                        {'label': 'Share by Volume', 'value': 'Share_by_Count'},
                                        {'label': 'Value/CPTO', 'value': 'Value'},
                                    ],
                                    value='Count',
                                    labelStyle={'display': 'block'}
                                )  
                            ])
                        ],
                        id='prediction-detail', 
                        style={'color': '#000000', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}),
                        
                        html.Details([
                            html.Summary('Product Filter', style={'font-weight': 'bold', 'color': '#000000'}),
                            # Category Filter
                            html.Label('Product Category:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-product-category',
                                    options=[{'label': i, 'value': i} for i in product_categories],
                                    value=[product_categories[0]],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Product Category',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ]),
                            # Product Name Filter
                            html.Label('Product Name:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-product-name',
                                    options=[{'label': i, 'value': i} for i in product_names],
                                    value=[product_names[0]],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Product Name',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ]),
                            # Shop Filter
                            html.Label('Shop:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-shop-name',
                                    options=[{'label': i, 'value': i} for i in shop_names],
                                    value=[shop_names[0]],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Shop Name',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ]),
                            # Brand Filter
                            html.Label('Brand:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-brand',
                                    options=[{'label': i, 'value': i} for i in []],
                                    value=[],
                                    disabled=True,
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Brand',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ]),
                            # Lot Size Filter
                            html.Label('Lot Size:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-lotsize',
                                    options=[{'label': i, 'value': i} for i in []],
                                    value=[],
                                    disabled=True,
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Lot Size',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ])
                        ], style={'color': '#000000', 'margin-top': '2vh', 'border':'1px white solid'}),
                        html.Br(),
                        
                        # Run Simulation
                        html.Div([
                            html.A(
                                dbc.Button("Run Simulation", 
                                        id='btn-run-simulation', 
                                        color="dark"), 
                            id='btn-run-anchor')
                        ], className="d-grid gap-2"),
                        html.Br(),
                        # Reset Pricing
                        html.Div([
                            html.A(
                                dbc.Button("Reset Simulator", 
                                        id='btn-reset-simulator', 
                                        color="dark"), 
                            id='btn-reset-anchor')
                        ], className="d-grid gap-2"),
                        html.Br(),
                        # Spinner To Show Simulation Status
                        html.Div(
                            id='spinner',
                            children=
                            [
                                # html.Img(src='data:image/gif;base64,{}'.format(spinner.decode())),
                                html.Label(
                                    id='spinner-label',
                                    children='Simualtion Progress: Pending....',
                                    style={'font-weight': 'bold', 'font-size': '16px', 'color': '#000000'}),
                            ], style={'display': 'none'},
                        ),
                    ], 
                    style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':10, 'marginRight':10}),
                    width=3, style={'backgroundColor':'#D3D3D3'}), 
            
                dbc.Col(html.Div([
                    dcc.Tabs(id="tabs", value='tab-1', style={'height': tab_height},
                        children=[
                            dcc.Tab(label='Retail Summary', value='tab-1', style={'padding': '0', 'line-height': tab_height}),
                            dcc.Tab(label='Pricing Input', value='tab-2', style={'padding': '0', 'line-height': tab_height}),
                            dcc.Tab(label='Product Sales', value='tab-3', style={'padding': '0', 'line-height': tab_height}),
                            dcc.Tab(label='Product KPIs', value='tab-4', style={'padding': '0', 'line-height': tab_height}),
                            dcc.Tab(label='Product KPIs Pivot', value='tab-5', style={'padding': '0', 'line-height': tab_height}),
                            dcc.Tab(label='Simulator Info', value='tab-6', style={'padding': '0', 'line-height': tab_height})
                        ])
                    , html.Div(id='tabs-content') #Setting default pricing input
                ]), width=9)
            ], className="h-85"),

            # Storing Components
            html.Div(
                children=[dcc.Store(id="storage-pricing-input"),
                        dcc.Store(id="storage-pricing-output")]
            ),

            # Hidden Divs to Store Asynchronous Task related
            html.Div([
                #  hidden div to store celery background job task-id, task-status, and message-status
                html.Div(id='task-id',
                        children=None,
                        style={'display': 'none'}
                        ),
                #  hidden div to store celery background job task-status
                html.Div(id='task-status',
                        children=None,
                        style={'display': 'none'}
                        ),
                #  page refresh interval
                dcc.Interval(
                    id='task-refresh-interval',
                    interval=24*60*60*1*1000,  # in milliseconds
                    n_intervals=0
                ),
            ])
        ],
        fluid=True,
        className="dbc")