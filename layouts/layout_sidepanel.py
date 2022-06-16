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
import dash_bootstrap_components as dbc 

# from backend import channel_type, analysis_type, granularity, maker_type, device_family, spinner
# from layouts import layout_retail_summary

tab_height = '7vh'
layout = html.Div([
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
                    width=9)
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
                                # start_date=custom_start_date,
                                # end_date=custom_end_date,
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
                                        {'label': 'Sticks (CIG)/ Gm (RYO)/ Items (NC)', 'value': 'Sticks'},
                                        {'label': 'Share by Volume', 'value': 'Share_Volume'},
                                        {'label': 'Value/CPTO', 'value': 'Value'},
                                        {'label': 'Share by Value/CPTO','value': 'Share_Value'},
                                        {'label': 'All','value': 'All'}
                                    ],
                                    value='Sticks',
                                    labelStyle={'display': 'block'}
                                )  
                            ])
                        ],
                        id='prediction-detail', 
                        style={'color': '#000000', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}),
                        
                        html.Details([
                            html.Summary('Product Filter', style={'font-weight': 'bold', 'color': '#000000'}),
                            # Category Filter
                            html.Label('Category:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-category',
                                    options=[{'label': i, 'value': i} for i in []],
                                    # options=[{'label': i, 'value': i} for i in category_type],
                                    value=[],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Category',
                                    style={
                                        'fontSize': '2vh',
                                        'color': 'black'
                                    }
                                )
                            ]),
                            # Manufacturer Filter
                            html.Label('Manufacturer:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-manufacturer',
                                    options=[{'label': i, 'value': i} for i in []],
                                    # options=[{'label': i, 'value': i} for i in manufacturer_type],
                                    value=[],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Maker',
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
                                    # options=[{'label': i, 'value': i} for i in brand_type],
                                    value=[],
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
                            # Pack Size Filter
                            html.Label('Pack Size:', style={'font-weight': 'bold', 'color': '#000000'}),
                            html.Div([
                                dcc.Dropdown(
                                    id='dd-packsize',
                                    options=[{'label': i, 'value': i} for i in []],
                                    # options=[{'label': i, 'value': i} for i in packsize_type],
                                    value=[],
                                    multi=True,
                                    clearable=True,
                                    searchable=False,
                                    placeholder='Select Pack Size',
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
                                    id='dd-productname',
                                    options=[{'label': i, 'value': i} for i in []],
                                    # options=[{'label': i, 'value': i} for i in productname_type],
                                    value=[],
                                    multi=True,
                                    clearable=True,
                                    searchable=True,
                                    placeholder='Select Product Name',
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
        ])