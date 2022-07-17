__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash_table as dt
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row(html.Label('Sticks: Expressed as Per 1000 Sticks', style={'font-size':'9px','font-weight': 'bold', 'color': '#000000'})),
                    dbc.Row(html.Label('Shares: Expressed as %age', style={'font-size':'9px','font-weight': 'bold', 'color': '#000000'})),
                    dbc.Row(html.Label('Value: Expressed as Canadian Dollars', style={'font-size':'9px','font-weight': 'bold', 'color': '#000000'})),
                ]),
                dbc.Col(dbc.Button(
                            "Download Predicted Sales", 
                            id='btn-download-sales', 
                            color="info", 
                            className="mr-1"),
                style={'text-align':'right'})
            ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),

            dbc.Row([
                dbc.Col(dt.DataTable(
                            id='datatable-output',
                            style_header={
                                    'whiteSpace': 'normal',
                                    'backgroundColor': '#172962',
                                    'color': 'white'
                                },
                            style_table={
                                'height': 350,
                                'overflowX': 'scroll',
                                'overflowY': 'scroll'
                            },
                            style_cell={
                                'fontSize': '1.5vh',
                                'textAlign': 'center',
                                "color": "black"
                                },
                            ), align="center")
            ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        # Province Output Filter
                        html.Label('Province:', style={'font-weight': 'bold', 'color': '#000000'}),
                        html.Div([
                            dcc.Dropdown(
                                id='dd-province-predicted',
                                # options=[{'label': i, 'value': i} for i in channel_type],
                                # value=channel_type[0],
                                multi=False,
                                searchable=False,
                                clearable=False,
                                placeholder='Select Output Channel',
                                style={
                                    'fontSize': '2vh',
                                    'color': 'black',
                                }
                            )
                        ])
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        # Province Output Filter
                        html.Label('Brand:', style={'font-weight': 'bold', 'color': '#000000'}),
                        html.Div([
                            dcc.Dropdown(
                                id='dd-brand-predicted',
                                # options=[{'label': i, 'value': i} for i in channel_type],
                                # value=channel_type[0],
                                multi=True,
                                searchable=False,
                                clearable=False,
                                placeholder='Select Brand',
                                style={
                                    'fontSize': '2vh',
                                    'color': 'black',
                                }
                            )
                        ])
                    ])
                ])
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),

            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='sbc-sales'
                        ),
                )
            ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
        ])