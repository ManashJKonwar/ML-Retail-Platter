__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from dash import no_update
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts import layout_retail_summary
from datasets.backend import df_transactions, df_products, df_shops

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='tabs-content', component_property='children'),
                        Input(component_id='tabs', component_property='value'))
def render_content(tab):
    if tab == 'tab-1':
        return layout_retail_summary.layout

@callback_manager.callback([Output(component_id='dd-product-name', component_property='options'),
                        Output(component_id='dd-product-name', component_property='value')],
                        Input(component_id='dd-shop-name', component_property='value'))
def set_product_options(sel_shop_names):
    if isinstance(sel_shop_names, list):
        sel_df_shop_names = df_shops.loc[df_shops.translated_shop_name.isin(sel_shop_names)].reset_index(drop=True)

        # Extracting transactions for selected shop names
        option_mask = (df_transactions.shop_id.isin(list(sel_df_shop_names.shop_id.unique())))
        sel_df_transactions = df_transactions.loc[option_mask].reset_index(drop=True)

        # Extracting final product options and setting default as first product
        final_options = sorted(list(df_products.loc[df_products.item_id.isin(list(sel_df_transactions.item_id.unique()))].translated_item_name.unique()))

        return final_options, [final_options[0]]
    else:
        return no_update     