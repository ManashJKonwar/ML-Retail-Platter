__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
import dash_table as dt
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html

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
                dbc.Col(html.A(dbc.Button(
                                    "Download Template", 
                                    id='btn-template', 
                                    color="info", 
                                    className="mr-1"), 
                                    id='template-btn-anchor',
                                    href="", 
                                    download="Japan Device Pricing Template.csv", 
                                    target="_blank"), width=3, style={'text-align':'center'}),
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
           
            # Addition of Sorting based Datatable
            dbc.Row([
                dbc.Col(dt.DataTable(
                            id='datatable-input',
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
                                # 'font-family': 'Arial',
                                'textAlign': 'center',
                                "color": "black"
                                },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['MAKER_DESCRIPTION','SUB_FAMILY_DESCRIPTION']],
                            style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{MODEL_FLAG} = "No"'
                                    },
                                    'backgroundColor': '#C2DFFF',
                                    'color': 'black'
                                }
                            ]
                            ), align="center")
            ], 
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
        ])