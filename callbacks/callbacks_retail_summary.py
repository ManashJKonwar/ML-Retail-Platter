__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import copy
import pandas as pd
from dash import html
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from datasets.backend import df_transactions, df_products, df_shops, df_product_categories

callback_manager = CallbackManager()

@callback_manager.callback(Output(component_id='p-salestext', component_property='children'),
                        [Input(component_id='dd-product-category', component_property='value'),
                        Input(component_id='dd-shop-name', component_property='value'),
                        Input(component_id='dd-product-name', component_property='value')])
def set_sales_card(sel_product_categories, sel_shop_names, sel_product_names):
    if isinstance(sel_product_categories, list) and isinstance(sel_shop_names, list) and isinstance(sel_product_names, list):
        sel_df_shop_names = df_shops.loc[df_shops.translated_shop_name.isin(sel_shop_names)].reset_index(drop=True)
        sel_df_product_names = df_products.loc[df_products.translated_item_name.isin(sel_product_names)].reset_index(drop=True)

        # Extracting transactions for selected shops and products
        transaction_mask = (df_transactions.shop_id.isin(list(sel_df_shop_names.shop_id.unique()))) & \
                        (df_transactions.item_id.isin(list(sel_df_product_names.item_id.unique()))) 

        sel_transactions = df_transactions.loc[transaction_mask].reset_index(drop=True)

        #Extracting total sales and return appropriate card body
        return "Total Sales: %s ₽" %(str(sum(sel_transactions.item_price * sel_transactions.item_cnt_day)))
    else:
        return no_update   

@callback_manager.callback(Output(component_id='p-categorytext', component_property='children'),
                        Input(component_id='dd-product-category', component_property='value'))
def set_category_card(sel_product_categories):
    if isinstance(sel_product_categories, list):
        # Condition for setting all product categories if none is selected
        if len(sel_product_categories) == 0:
            sel_product_categories = sorted(list(df_product_categories.translated_item_category_name.unique()))

        sel_df_product_categories = df_product_categories.loc[df_product_categories.translated_item_category_name.isin(sel_product_categories)].reset_index(drop=True)

        # Extracting item category id and extracting the respective item ids
        item_mask = df_products.item_category_id.isin(list(sel_df_product_categories.item_category_id.unique()))
        sel_df_product = df_products.loc[item_mask].reset_index(drop=True)

        # Extracting transactions for selected products
        transaction_mask = (df_transactions.item_id.isin(list(sel_df_product.item_id.unique())))
        sel_transactions = df_transactions.loc[transaction_mask].reset_index(drop=True) 
       
        # Merged transactions data
        final_sel_transactions = pd.merge(pd.merge(sel_transactions, sel_df_product, how='left', on='item_id'), df_product_categories[['item_category_id','translated_item_category_name']], how='left', on='item_category_id')
        final_sel_transactions = final_sel_transactions[['date', 'item_price', 'item_cnt_day', 'translated_item_category_name']]

        # Grouping by highest sales for each product category
        final_grp_transactions = final_sel_transactions.groupby('translated_item_category_name').agg({'item_cnt_day':'sum'}).reset_index()
        final_grp_transactions = final_grp_transactions.rename(columns={'item_cnt_day':'total_no_products_sold'})
        final_grp_transactions = final_grp_transactions.sort_values('total_no_products_sold', ascending=False).reset_index(drop=True)

        return [
                "Best Category: %s" %(final_grp_transactions.head(1).translated_item_category_name[0]),
                html.Br(),
                "Total no of products sold within this category: %s" %(str(final_grp_transactions.head(1).total_no_products_sold[0]))
            ]
    else:
        return no_update

@callback_manager.callback(Output(component_id='p-producttext', component_property='children'),
                        Input(component_id='dd-product-name', component_property='value'),
                        State(component_id='dd-product-name', component_property='options'))
def set_category_card(sel_product, avail_product):
    if isinstance(sel_product, list):
        # Condition for setting all products if none is selected
        if len(sel_product) == 0:
            sel_product = copy.deepcopy(avail_product)

        sel_df_product = df_products.loc[df_products.translated_item_name.isin(sel_product)].reset_index(drop=True)

        # Extracting respective item ids from transaction data
        product_mask = df_transactions.item_id.isin(list(sel_df_product.item_id.unique()))
        sel_df_transactions = df_transactions.loc[product_mask].reset_index(drop=True)

        # Summing up total revenue accumulated by selling these products
        sel_df_transactions['item_sales'] = sel_df_transactions['item_price'] * sel_df_transactions['item_cnt_day']
        sel_df_transactions['item_sales'] = sel_df_transactions['item_sales'].apply(lambda x : x if x > 0 else 0)

        # Grouping by highest sales for each product id
        final_grp_transactions = sel_df_transactions.groupby('item_id').agg({'item_sales':'sum'}).reset_index()

        # Merging transactions data
        final_sel_transactions = pd.merge(final_grp_transactions, df_products[['item_id','translated_item_name']], how='left', on='item_id')
        final_sel_transactions = final_sel_transactions.sort_values('item_sales', ascending=False).reset_index(drop=True)

        return [
                "Best Product: %s" %(final_sel_transactions.head(1).translated_item_name[0]),
                html.Br(),
                "Total sales for this product: %s ₽" %(str(final_sel_transactions.head(1).item_sales[0]))
            ]
    else:
        return no_update

@callback_manager.callback(Output(component_id='p-shoptext', component_property='children'),
                        Input(component_id='dd-shop-name', component_property='value'),
                        State(component_id='dd-shop-name', component_property='options'))
def set_category_card(sel_shops, avail_shops):
    if isinstance(sel_shops, list):
        # Condition for setting all products if none is selected
        if len(sel_shops) == 0:
            sel_shops = copy.deepcopy(avail_shops)

        sel_df_shop = df_shops.loc[df_shops.translated_shop_name.isin(sel_shops)].reset_index(drop=True)

        # Extracting respective shops ids and getting relevant transaction data
        shop_mask = df_transactions.shop_id.isin(list(sel_df_shop.shop_id.unique()))
        sel_df_transactions = df_transactions.loc[shop_mask].reset_index(drop=True)

        # Summing up total revenue accumulated by selling from these shops
        sel_df_transactions['item_sales'] = sel_df_transactions['item_price'] * sel_df_transactions['item_cnt_day']
        sel_df_transactions['item_sales'] = sel_df_transactions['item_sales'].apply(lambda x : x if x > 0 else 0)

        # Grouping by highest sales for each product id
        final_grp_transactions = sel_df_transactions.groupby('shop_id').agg({'item_sales':'sum'}).reset_index()

        # Merging transactions data
        final_sel_transactions = pd.merge(final_grp_transactions, df_shops[['shop_id','translated_shop_name']], how='left', on='shop_id')
        final_sel_transactions = final_sel_transactions.sort_values('item_sales', ascending=False).reset_index(drop=True)

        return [
                "Best Store: %s" %(final_sel_transactions.head(1).translated_shop_name[0]),
                html.Br(),
                "Total sales from this shop: %s ₽" %(str(final_sel_transactions.head(1).item_sales[0]))
            ]
    else:
        return no_update