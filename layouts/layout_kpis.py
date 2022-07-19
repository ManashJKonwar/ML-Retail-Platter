__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

layout = html.Div([
            dbc.Row([
                dbc.Col(html.A(dbc.Button(
                                    "Add KPI Widgets", 
                                    id='add-kpi-widgets', 
                                    color="info", 
                                    outline=True,
                                    className="mr-1"),
                                    id='add-kpi-btn-anchor'),
                style={'text-align':'left'})
            ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),

            html.Div(id='kpi-widget-container', children=[],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10})
        ])

def get_kpi_widget_template(n_clicks):
    new_child = html.Div(
        style={'width': '100%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Line Chart', 'value': 'line'},
                         {'label': 'Pie Chart', 'value': 'pie'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dd-shop',
                    'index': n_clicks
                },
                multi=True
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dd-kpi',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in ['Product Volume', 'Product Profit', 'SOP']],
                value='Product Volume'
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Label(
                        id={
                            'type': 'dynamic-historic-value',
                            'index': n_clicks
                        }
                    )
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label(
                        id={
                            'type': 'dynamic-predicted-value',
                            'index': n_clicks
                        }
                    )
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label(
                        id={
                            'type': 'dynamic-change-value',
                            'index': n_clicks
                        }
                    )
                ])
            ])
        ]
    )
    return new_child