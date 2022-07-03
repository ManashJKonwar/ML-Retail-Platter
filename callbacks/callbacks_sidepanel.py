__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import copy
from dash import no_update
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from layouts import layout_retail_summary, layout_pricing_input
from datasets.backend import df_transactions, df_products, df_shops, df_product_categories

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='tabs-content', component_property='children'),
                        Input(component_id='tabs', component_property='value'))
def render_content(tab):
    if tab == 'tab-1':
        return layout_retail_summary.layout
    elif tab == 'tab-2':
        return layout_pricing_input.layout

@callback_manager.callback([Output(component_id='dd-product-name', component_property='options'),
                        Output(component_id='dd-product-name', component_property='value')],
                        Input(component_id='dd-product-category', component_property='value'))
def set_product_options(sel_product_categories):
    if isinstance(sel_product_categories, list):
        # Condition for setting all product categories if none is selected
        if len(sel_product_categories) == 0:
            sel_product_categories = sorted(list(df_product_categories.translated_item_category_name.unique()))

        sel_df_product_categories = df_product_categories.loc[df_product_categories.translated_item_category_name.isin(sel_product_categories)].reset_index(drop=True)

        # Extracting product names based on product categories
        product_mask = df_products.item_category_id.isin(list(sel_df_product_categories.item_category_id.unique()))
        sel_df_product = df_products.loc[product_mask].reset_index(drop=True)

        # Extracting final product options and setting default as first product
        final_options = sorted(list(sel_df_product.translated_item_name.unique()))

        return final_options, [final_options[0]]
    else:
        return no_update 

@callback_manager.callback([Output(component_id='dd-shop-name', component_property='options'),
                        Output(component_id='dd-shop-name', component_property='value')],
                        Input(component_id='dd-product-name', component_property='value'),
                        State(component_id='dd-product-name', component_property='options'))
def set_product_options(sel_product_names, avail_products):
    if isinstance(sel_product_names, list):
        # Condition for setting all products if none is selected
        if len(sel_product_names) == 0:
            sel_product_names = copy.deepcopy(avail_products)

        sel_df_product = df_products.loc[df_products.translated_item_name.isin(sel_product_names)].reset_index(drop=True)

        # Extracting shop ids based on product names
        shop_mask = df_transactions.item_id.isin(list(sel_df_product.item_id.unique()))
        sel_df_transactions = df_transactions.loc[shop_mask].reset_index(drop=True)

        # Extracting shop names based on extracted shop ids
        shop_id_list = sorted(list(sel_df_transactions.shop_id.unique()))
        sel_df_shop = df_shops.loc[df_shops.shop_id.isin(shop_id_list)].reset_index(drop=True)

        # Extracting final shop optons and setting default as first shop
        final_options = sorted(list(sel_df_shop.translated_shop_name.unique()))

        return final_options, [final_options[0]]
    else:
        return no_update

@callback_manager.callback([Output(component_id='simulation-detail', component_property='style'),
            Output(component_id='prediction-detail', component_property='style')],
            Input(component_id='tabs', component_property='value'))
def render_side_filter(tab):
    if tab == 'tab-2':
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        return simulation_detail_style, prediction_detail_style
    elif tab == 'tab-3':
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'block'}
        return simulation_detail_style, prediction_detail_style
    else:
        simulation_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        prediction_detail_style = {'color': '#ffffff', 'margin-top': '2vh', 'border':'1px white solid', 'display':'None'}
        return simulation_detail_style, prediction_detail_style