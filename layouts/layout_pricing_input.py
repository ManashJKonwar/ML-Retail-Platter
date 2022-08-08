__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table as dt

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Simulation Input Type:"),
                    dbc.RadioItems(
                        options=[
                            {"label": "Manual Input", "value": "Manual Input"},
                            {"label": "Upload Input", "value": "Upload Input"}
                        ],
                        value="Manual Input",
                        id="radioitems-sim-input-type",
                        inline=True
                    )
                ])
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
            
            dbc.Row([
                dbc.Col(html.A(dcc.Upload(
                                    id='upload-data',
                                    children=html.Div(['Drag and Drop Simulation Input Data']),
                                    style={'width': '100%','height': '60px','lineHeight': '60px','borderWidth': '1px','borderStyle': 'dashed', \
                                        'borderRadius': '5px','textAlign': 'center','margin': '10px'},
                                    # Allow multiple files to be uploaded is set to one
                                    multiple=False
                                ), id='upload-region-anchor'), width=9, style={'text-align':'center'}),
                dbc.Col(
                    dbc.Button(
                            "Download Pricing Template", 
                            id='btn-template-pricing', 
                            color="info", 
                            className="mr-1"),
                    style={'text-align':'center'})
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
           
            # Addition of Sorting based Datatable
            dbc.Row([
                dbc.Col(dt.DataTable(
                            id='datatable-input',
                            editable=True,
                            style_header={
                                    'whiteSpace': 'normal',
                                },
                            style_table={
                                'height': 450,
                                'overflowX': 'scroll',
                                'overflowY': 'scroll'
                            },
                            style_cell={
                                'fontSize': '1.5vh',
                                'textAlign': 'center',
                            },
                            style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['PARENT_CATEGORY','PRODUCT_CATEGORY','PRODUCT','SHOP']],
                        ), 
                        align="center"
                    )
                ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
        ])