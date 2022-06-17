__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash_html_components as html
import dash_bootstrap_components as dbc

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

layout = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card(card_content, color="primary", inverse=True)
                ),
                dbc.Col(
                    dbc.Card(card_content, color="secondary", inverse=True)
                ),
                dbc.Col(
                    dbc.Card(card_content, color="info", inverse=True)
                ),
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
        ])