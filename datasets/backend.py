__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
from utility.utility_data_transformation import long_term_structure, short_term_structure, get_custom_dates

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
# Generating date month map
df_date_week_map = df_transactions[['date', 'date_block_num']].copy().drop_duplicates().reset_index(drop=True)
df_date_week_map['date'] = pd.to_datetime(df_date_week_map['date'], infer_datetime_format=True, format='%d.%m.%Y')
df_date_week_map['year'] = df_date_week_map.date.apply(lambda x: x.year)
df_date_week_map['month'] = df_date_week_map.date.apply(lambda x: x.month)
df_date_week_map = df_date_week_map[['year', 'month','date_block_num']].drop_duplicates().reset_index(drop=True)
df_date_week_map['date'] =  pd.to_datetime(dict(year=df_date_week_map.year, month=df_date_week_map.month, day='01'))

# Generating consolidated data
df_consolidated = df_transactions.copy()
df_consolidated['date'] = pd.to_datetime(df_consolidated['date'], infer_datetime_format=True, format='%d.%m.%Y')
df_consolidated = df_consolidated.groupby(['shop_id','item_id'], as_index=False)[['date_block_num','item_price','item_cnt_day']].max('date').reset_index(drop=True)
df_consolidated = pd.merge(df_consolidated, df_date_week_map, how='left', on='date_block_num')[['date', 'shop_id', 'item_id', 'date_block_num', 'item_price', 'item_cnt_day']].reset_index(drop=True)

# Merging item names and shop names with consolidated data
df_consolidated = pd.merge(df_consolidated, df_products[['item_id','item_category_id','translated_item_name']], how='left', on='item_id').reset_index(drop=True)
df_consolidated = pd.merge(df_consolidated, df_product_categories[['item_category_id','translated_item_category_name']], how='left', on='item_category_id').reset_index(drop=True)
df_consolidated = pd.merge(df_consolidated, df_shops[['shop_id','translated_shop_name']], how='left', on='shop_id').reset_index(drop=True)

# Renaming columns properly
df_consolidated.rename(columns={'translated_item_name':'PRODUCT', 'translated_shop_name':'SHOP', 'translated_item_category_name':'PRODUCT_CATEGORY', \
                    'item_price':'PRICE_PER_ITEM'}, inplace=True)
df_consolidated = df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']]
#endregion  

#region Generic functions
lt_month_range, lt_month2week_list = long_term_structure()
st_month_range, st_month2week_list = short_term_structure()
custom_start_date, custom_end_date = get_custom_dates()
#endregion