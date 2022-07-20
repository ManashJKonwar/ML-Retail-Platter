__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pickle
import pandas as pd
from datetime import datetime, timedelta
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

#region Inferencing pipeline related
derived_features_list = []
with open(r'datasets\new_features.pkl', 'rb') as feature_file:
    derived_features_list = pickle.load(feature_file)

def generate_features_df(features_list=[]):
    df_features = pd.DataFrame(columns=['feature_name','feature_type','price_dependency']) 
    try:
        # Form a dataframe which maps each feature to type of it and whether it is 
        # dependent on price change or not
        for feature in features_list:
            feature_type, price_dependency = '', False
            # Segregating features
            feature_splitted_list = feature.split('_')
            if 'sales' in feature_splitted_list or 'cnt' in feature_splitted_list:
                feature_type = 'sales'
            elif 'price' in feature_splitted_list:
                feature_type = 'price'
                price_dependency = True
            elif 'tfidf' in feature_splitted_list:
                feature_type = 'text'
            else:
                if 'date' in feature_splitted_list:
                    feature_type = 'month'
                else:
                    feature_type = 'id'

            intermediate_features = pd.DataFrame.from_records([{'feature_name': feature, 'feature_type': feature_type, 'price_dependency': price_dependency}])
            df_features = pd.concat([df_features, intermediate_features], ignore_index=True)
        
        return df_features
    except Exception as ex:
        print('Caught Exception while generating features dataframe as: %s' %(str(ex)))
        pass

df_features = generate_features_df(features_list=['shop_id', 'item_id', 'item_category_id', 'date_block_num', 'item_price'] + derived_features_list)
df_variable_type = df_features.copy().reset_index(drop=True)
df_features['MODEL_ID'] = 'MODEL_01'
df_features = df_features.reset_index(drop=True)

# Extract the xvars for last training month i.e. date_block_num == 33
df_xvar = pd.read_csv('datasets\latest_dataset.csv')

# Extracting the maps
dict_product_category_id_map = {row.item_category_name: row.item_category_id for row in pd.read_csv('datasets\item_categories_map.csv').itertuples()}
dict_product_id_map = {row.translated_item_name: row.item_id for row in df_products[['item_id','translated_item_name']].drop_duplicates().itertuples()}
dict_shop_id_map = {row.translated_shop_name: row.shop_id for row in df_shops[['shop_id','translated_shop_name']].drop_duplicates().itertuples()}
#endregion

#region KPI widgetting
# Extracting week, year and month information from transaction dates
df_transactions_weekly = df_transactions.copy()
df_transactions_weekly['date'] = pd.to_datetime(df_transactions_weekly['date'], infer_datetime_format=True, format='%d.%m.%Y')
df_transactions_weekly['week'] = df_transactions_weekly.date.dt.isocalendar().week
df_transactions_weekly['month'] = df_transactions_weekly.date.dt.month
df_transactions_weekly['year'] = df_transactions_weekly.date.dt.year
df_transactions_weekly['week_start_date'] = df_transactions_weekly.date.apply(lambda x: x - timedelta(days=x.weekday()))

# Grouping item prices based on grouby selections
df_transactions_weekly = df_transactions_weekly.groupby(['week_start_date','year','shop_id','item_id']).agg({'item_price':'mean'}).reset_index()

# Merging item names and shop names with consolidated data
df_transactions_weekly = pd.merge(df_transactions_weekly, df_products[['item_id','item_category_id','translated_item_name']], how='left', on='item_id').reset_index(drop=True)
df_transactions_weekly = pd.merge(df_transactions_weekly, df_product_categories[['item_category_id','translated_item_category_name']], how='left', on='item_category_id').reset_index(drop=True)
df_transactions_weekly = pd.merge(df_transactions_weekly, df_shops[['shop_id','translated_shop_name']], how='left', on='shop_id').reset_index(drop=True)

# Renaming columns properly
df_transactions_weekly = df_transactions_weekly.rename(columns={'translated_item_name':'product_name', 'translated_item_category_name':'product_category', 'translated_shop_name':'shop_name'})
#endregion