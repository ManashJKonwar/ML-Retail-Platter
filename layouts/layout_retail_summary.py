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

sales_card = dbc.Card([
                dbc.CardBody([
                    html.H5("Sales Card", className="card-title"),
                    html.P(
                        "Total Sales: %s ₽" %(str(500)),
                        id='p-salestext',
                        className="card-text",
                    ),
                ]
            )], color="secondary", inverse=True)

category_card = dbc.Card([
                dbc.CardBody([
                    html.H5("Category Card", className="card-title"),
                    html.P([
                        "Best Category: %s" %('Accessories'),
                        html.Br(),
                        "Total no of products sold within this category: %s" %(str(50))],
                        id='p-categorytext',
                        className="card-text",
                    ),
                ]
            )], color="secondary", inverse=True)

product_card = dbc.Card([
                dbc.CardBody([
                    html.H5("Product Card", className="card-title"),
                    html.P([
                        "Best Product: %s" %('Ps4'),
                        html.Br(),
                        "Total sales for this product: %s ₽" %(str(50))],
                        id='p-producttext',
                        className="card-text",
                    ),
                ]
            )], color="secondary", inverse=True)

shop_card = dbc.Card([
                dbc.CardBody([
                    html.H5("Shopping Card", className="card-title"),
                    html.P([
                        "Best Store: Fancy Store",
                        html.Br(),
                        "Total Sales Count: %s" %(str(200))],
                        id='p-shoptext',
                        className="card-text",
                    ),
                ]
            )], color="secondary", inverse=True)

layout = html.Div([
            dbc.Row([
                dbc.Col(sales_card),
                dbc.Col(category_card),
                dbc.Col(product_card),
                dbc.Col(shop_card)
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),
        ])