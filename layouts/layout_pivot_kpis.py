__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash_pivottable
from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
            dbc.Row([
                dbc.Col(
                    dash_pivottable.PivotTable(
                        id='pivot-table',
                        cols=['WEEK_DATE'],
                        rows=['PRODUCT_CATEGORY','PRODUCT','SHOP'],
                        rendererName='Grouped Column Chart',
                        aggregatorName='Sum',
                        vals=['SALES_VOLUME']
                    ),
                )
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10}),

            dbc.Row([
                dbc.Col(
                    html.Div(
                        id='pivotting-output'
                    )
                )
            ],
            style={'marginBottom': 10, 'marginTop': 10, 'marginLeft':10, 'marginRight':10})
        ], 
        style={'overflow-x':'scroll'})

def get_pivot_table_children(**kwargs):
    cols = kwargs.get('cols')
    rows = kwargs.get('rows')
    row_order = kwargs.get('row_order')
    col_order = kwargs.get('col_order')
    aggregator = kwargs.get('aggregator')
    renderer = kwargs.get('renderer')
    
    return [
        html.P(str(cols), id='columns'),
        html.P(str(rows), id='rows'),
        html.P(str(row_order), id='row_order'),
        html.P(str(col_order), id='col_order'),
        html.P(str(aggregator), id='aggregator'),
        html.P(str(renderer), id='renderer'),
    ]