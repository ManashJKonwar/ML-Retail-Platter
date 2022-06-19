__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd

#region Reading Main Dataframes
df_product_categories = pd.read_csv(r'datasets\translated_item_categories.csv')
df_products = pd.read_csv(r'datasets\translated_items.csv')
df_shops = pd.read_csv(r'datasets\translated_shops.csv')
df_transactions = pd.read_csv(r'datasets\sales_train.csv')
#endregion

#region Sidepanel Options
product_categories = sorted(list(df_product_categories.translated_item_category_name.unique()))
product_names = sorted(list(df_products.translated_item_name.unique()))
shop_names = sorted(list(df_shops.translated_shop_name.unique()))
#endregion

#region Data Preprocessing
print('here')
#endregion  