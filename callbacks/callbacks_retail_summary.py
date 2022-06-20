__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from dash.dependencies import Input, Output
from callback_manager import CallbackManager
from datasets.backend import df_transactions, df_products, df_shops

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
        return "Total Sales: %s Mn" %(str(sum(sel_transactions.item_price * sel_transactions.item_cnt_day)))
    else:
        return no_update   