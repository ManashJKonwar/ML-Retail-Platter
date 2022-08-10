__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
import copy
import math
import pickle
import datetime
import pandas as pd

class PredictSalesModel():
    def __init__(self, *args, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        self._row_info_data = kwargs.get('row_info_data') # Stores Column name list and relevant row data wrt column names
        self._historic_df = kwargs.get('historic_df') # Stores Historic Consolidated data wrt Province + Brand Combination
        self._consolidated_df = kwargs.get('consolidated_df') # Stores Latest Consolidated data wrt Province + Brand Combination
        self._pricing_df = kwargs.get('pricing_df') # Pricing Input Table as Dataframe
        self._features_df = kwargs.get('features_df') # Significant Features Dataframe
        self._xvar_df = kwargs.get('xvar_df') # Variable Values for Significant Features
        self._comp_rank_df = kwargs.get('comp_rank_df') # Competitor rank for Province + Brand Combination
        self._overriden_xvar_dict = kwargs.get('overridden_xvars_dict') # Dictionary of Overriding Xvars
        self._variable_type_df = kwargs.get('variable_type_df') # Get Variable Type Dataframe
        self._model_endpoints_df = kwargs.get('model_endpoints_df') # Model Endpoint Registry Name Dataframe
        self._model_endpoints_dict = kwargs.get('model_endpoints_dict') # Endpoint for Linear, Lasso, Ridge, Elastic Models
        self._model_picklefile_dict = kwargs.get('model_picklefile_dict') # Model Pickle Mapper wrt Province + Brand Combination
        self._mapping_dict = kwargs.get('mapping_dict') # Provides map of ids of categories, products and relevant shops
        self._product_info_dict = kwargs.get('product_info_dict') # Stores Info about products for which simulation needs to be fired
        self._month_to_weeks = kwargs.get('month_to_weeks') # Month to Week Mapping
        self._pickle_flag = kwargs.get('pickle_flag') # Model to predict from pickle files or model endpoints
        self._logger = kwargs.get('logger') # Logger Object for logging operational steps
        
        '''
        self._model_uri, self._bearer_key, self._reg_model_name = self.map_model_endpoint() # Extracts Model URL for respective Province + Brand Combination
        self._model_comp = self.map_model_comp() # Extracts competitor rank data based on Province + Brand i.e. irrespective of KA it is constant 
        self._combined_own_df, self._combined_comp_df = self.split_historic_df() # Extracts Own and Competitor Consolidate Price Per Stick
        '''
        self._model_pkl = self._map_model_picklefile() # Extracts Name of Pickle file for respective data granularity (category+product+shop)
        self._features_dict = self._map_features() # Extracts Significant features for the respective data granularity (category+product+shop) in a dictionary with latest values
        self._consolidated_data = self._extract_consolidated_data()

        self._final_data_dict = {'data':[]} 

    def _map_model_picklefile(self):
        """
        This method maps model pickle file and extracts name of pickle file to refer
        Parameters: 
            None
        Returns: 
            pickle_file_name (str): name of the pickle file based on combination of Province and Brand
        """
        try:
            return self._model_picklefile_dict[self._product_info_dict['PARENT']]
        except Exception:
            return None

    def _map_features(self):
        """
        This method helps in extracting significant features for each model based on xvar indexes utilized
        while training the model
        Parameters: 
            None
        Returns: 
            feature_dict (dict, (dict, str)): Extracts all significant features with respect to Province
                                            and Brand Combination and presents in order of value and 
                                            category of each feature
        """
        feature_dict={}

        try:
            # Masking features related to only specific Province and Brand from features dataframe
            feature_extraction_mask = (self._features_df.group_name==self._product_info_dict['PARENT'])
            feature_data = self._features_df.loc[feature_extraction_mask].reset_index(drop=True)

            xvar_extraction_mask = (self._xvar_df.parent_category_name.isin([self._product_info_dict['PARENT']])) & \
                            (self._xvar_df.item_category_id.isin([self._mapping_dict['category'][self._product_info_dict['CATEGORY']]])) & \
                            (self._xvar_df.shop_id.isin([self._mapping_dict['shop'][self._product_info_dict['SHOP']]])) & \
                            (self._xvar_df.item_id.isin([self._mapping_dict['product'][self._product_info_dict['PRODUCT']]]))
            consolidated_data = self._xvar_df.loc[xvar_extraction_mask].drop_duplicates(keep=False).reset_index(drop=True)
            
            for row in feature_data.itertuples():
                if row.feature_name not in feature_dict.keys():
                    if math.isnan(consolidated_data[row.feature_name][0]):
                        feature_dict[row.feature_name] = {'value':0.0, 'feature_type': row.feature_type}
                    else:
                        feature_dict[row.feature_name] = {'value':consolidated_data[row.feature_name][0], 'feature_type': row.feature_type}
            self._logger.info('Feature Extraction Done Successfully')
            return feature_dict
        except Exception as ex:
            raise ex

    def _extract_consolidated_data(self):
        consolidated_mask = (self._consolidated_df.PARENT_CATEGORY.isin([self._product_info_dict.get('PARENT')])) & \
                            (self._consolidated_df.PRODUCT_CATEGORY.isin([self._product_info_dict.get('CATEGORY')])) & \
                            (self._consolidated_df.PRODUCT.isin([self._product_info_dict.get('PRODUCT')])) & \
                            (self._consolidated_df.SHOP.isin([self._product_info_dict.get('SHOP')]))
        return self._consolidated_df.loc[consolidated_mask].reset_index(drop=True)

    def input_data_build(self, period_type='Quarterly'):
        """
        This method helps in generating input as per granularity for which the prediction is run for. We have
        3 options: Quarterly, Annualy and Custom
        Parameters: 
            period_type (str): Quarterly, Annualy or Custom (Default Value is Quarterly)
        Returns: 
            df_own (pandas dataframe): Model Under consideration data
            df_comp (pandas dataframe): Competitor Model data with respect to model under consideration
        """
        #self._logger.info('Generating Input Data Started')
        # Populating local data dictionary variable
        data_dict={}
        if period_type.__eq__('Quarterly') or period_type.__eq__('Custom'):
            # Plain Execution of Weekly Level Data Provided
            counter = 5
            column_name_list, row_data = self._row_info_data[0], self._row_info_data[1]
            for item in column_name_list[5:]:
                try:
                    data_dict[item] = float(eval("row_data._"+str(counter)))
                    counter+=1

                except Exception as ex:
                    counter+=1
                    continue
        elif period_type.__eq__('Annually'):
            # Plain Execution of Monthly Level Data Provided
            counter = 5
            column_name_list, row_data = self._row_info_data[0], self._row_info_data[1]
            month_map={}
            for item in column_name_list[5:]:
                try:
                    item_year_month = '-'.join(item.split('-')[0:2])
                    month_map[item_year_month] = [x for x in self._month_to_weeks if '-'.join(x.split('-')[0:2]) == item_year_month]
                    if len(month_map[item_year_month])>0:
                        for value in month_map[item_year_month]:
                            data_dict[value] = float(eval("row_data._"+str(counter)))
                    counter+=1
                except Exception as ex:
                    counter+=1
                    continue
        
        # Populating final data
        for key in data_dict.keys():
            row_dict = copy.deepcopy(self._features_dict)
            # Overridding Price Per Item Value based on user Input
            if 'item_price' in row_dict.keys():
                row_dict['item_price']['value'] = float(data_dict[key])
            
            # Overridding Trend Variable/Date Block No by Dynamically Calculated Value
            if 'date_block_num' in row_dict.keys():
                key_date = datetime.datetime.strptime(key, '%Y-%b-%d').date()
                start_date = datetime.datetime.strptime('2013-01-01', '%Y-%m-%d').date()
                row_dict['date_block_num']['value'] = (key_date.year - start_date.year) * 12 + key_date.month - start_date.month

            if 'week_block_num' in row_dict.keys():
                key_date = datetime.datetime.strptime(key, '%Y-%b-%d').date()
                start_date = datetime.datetime.strptime('2012-12-31', '%Y-%m-%d').date()
                row_dict['week_block_num']['value'] = (abs(key_date - start_date).days)//7

            if 'month' in row_dict.keys():
                row_dict['month']['value'] = int(datetime.datetime.strptime(key, '%Y-%b-%d').date().month)
            
            # Modifying Seasonality and Weather Data
            row_dict = self.modify_backend_xvars(row_dict=row_dict, week_date=key)
            # Modifying Pricing Ratios
            row_dict = self.modify_pricing_interactions(period_type=period_type, row_dict=row_dict, week_date=key)
            '''
            # Modifying Lag Features
            row_dict = self.modify_lag_features(period_type=period_type, row_dict=row_dict, week_date=key)
            # Modifying Log Features # This needs to be the ending step of modifying it since we were playing with absolute values
            # till now
            row_dict = self.modify_log_features(row_dict=row_dict)
            '''
            # Adding to final data dictionary
            self._final_data_dict['data'] += [[x['value'] for x in list(row_dict.values())]]
        
        self._logger.info('Generating Input Data Done Successfully with data length: %s' %(str(len(self._final_data_dict['data']))))

    def modify_backend_xvars(self, row_dict=None, week_date=None):
        """
        This method helps in modifying any backend xvars which are independent of price changes made by user and 
        are more dependent on duration for which the prediction is made for
        Parameters: 
            row_dict (dict, (dict, str)): dictionary of all features as key and respective value and category
                                        extracted for each of these features
            week_date (str): week date for which prediction is supposed to be made
        Returns: 
            row_dict (dict, (dict, str)): Modified features Dictionary. Overriden Xvars are:
                                        1. Seasonality Data (SEASONALITY_INDEX)
                                        2. Weather Data (AVG_TEMP)
        """
        # Extract Week No based on week_date provided for that specific year
        month_no = datetime.datetime.strptime(week_date, '%Y-%b-%d').date().month
        def seasonality_weather_update():
            seasonality_weather_mask = (self._overriden_xvar_dict['seasonality_weather_df'].parent_category_name.isin([self._product_info_dict['PARENT']])) &\
                                    (self._overriden_xvar_dict['seasonality_weather_df'].month.isin([month_no]))
            seasonality_weather_data = self._overriden_xvar_dict['seasonality_weather_df'].loc[seasonality_weather_mask].reset_index(drop=True)
            
            # Check if updation is actually required or not
            if len(seasonality_weather_data) == 0:
                return row_dict
            for xvar in row_dict.keys():
                try:
                    if row_dict[xvar]['feature_type'].__eq__('seasonality') and xvar.__eq__('seasonal_index'):
                        row_dict[xvar]['value'] = round(float(seasonality_weather_data['seasonal_index'][0]),3)
                    elif row_dict[xvar]['feature_type'].__eq__('weather') and xvar.__eq__('avg_temp'):
                        row_dict[xvar]['value'] = float(seasonality_weather_data['avg_temp'][0])
                except Exception as ex:
                    self._logger.error('Modifying Backend XVars Caught Exception as: '+str(ex), exc_info=True)
                    continue
            return row_dict

        for backend_data in self._overriden_xvar_dict.keys():
            # Check if the backend data thats need updation is seasonality and weather data
            if backend_data.__eq__('seasonality_weather_df'):
                row_dict = seasonality_weather_update()
        
        return row_dict

    def modify_pricing_interactions(self, period_type='Quarterly', row_dict=None, week_date=None):
        """
        This method helps in modifying price ratios based on user provided values for self and also takes 
        into consideration any competitor price to capture the effect of product cannabilism
        Parameters: 
            period_type (str): Quarterly, Annualy or Custom (Default Value is Weekly)
            row_dict (dict, (dict, str)): dictionary of all features as key and respective value and category
                                        extracted for each of these features
            week_date (str): week date for which prediction is supposed to be made
        Returns: 
            row_dict (dict, (dict, str)): Modified features Dictionary. Overriden Xvars are:
        """
        if period_type.__eq__('Annually'):
            week_date='-'.join(week_date.split('-')[:2]) + '-01'

        for xvar in row_dict.keys():
            try:
                # Check if the xvar iterated is competitor own price ratio
                if row_dict[xvar]['feature_type'].__eq__('price ratio') and xvar != 'priceratio_parent_category':
                    competitor_category_id = xvar.split('_')[3]
                    competitor_category_name = self._mapping_dict.get('category_inv').get(int(competitor_category_id))
                    
                    # Check if prices exists in current pricing df
                    price_extraction_mask = (self._pricing_df.PRODUCT_CATEGORY==competitor_category_name)
                    pricing_data = self._pricing_df.loc[price_extraction_mask].reset_index(drop=True)
                    
                    if len(pricing_data)>0:
                        # Perform Dynamic Price Ratio Creation Based on User Input Prices
                        # print('Dynamic Price Ratio (from Pricing Input) Variable: %s for Parent Categry: %s and Product Category: %s' %(xvar, 
                        #                                                                                                               self._product_info_dict['PARENT'],
                        #                                                                                                                   self._product_info_dict['CATEGORY'])
                        # )
                        # Extracting Value from Pricing Data
                        comp_cat_price = float(pd.to_numeric(pricing_data[week_date]).mean())
                        own_price = row_dict['item_price']['value']
                        price_ratio = own_price/comp_cat_price
                        row_dict[xvar]['value'] = price_ratio
                    else:
                        # Perforn Dynamic Price Ratio Creation Based on Default Prices from Consolidated Data
                        # print('Dynamic Price Ratio (from Consolidated Data) Variable: %s for Province: %s and Brand: %s' %(xvar, 
                        #                                                                         self._province_brand_dict['PROVINCE'],
                        #                                                                         self._province_brand_dict['BRAND'])
                        # )
                        # Extracting Value from Conslidated Data
                        competitor_consolidated_mask = (self._consolidated_df.PROVINCE==competitor_data.PROVINCE[0]) &\
                                                        (self._consolidated_df.BRAND_AGG==competitor_data.BRAND_AGG[0])
                        competitor_consolidated_data = self._consolidated_df.loc[competitor_consolidated_mask].reset_index(drop=True)

                        # Calculating Price Ratio and replacing the value in row level dictionary
                        if len(competitor_consolidated_data)>0:
                            comp_price = competitor_consolidated_data.AVE_PRICE_STICK[0]
                            own_price = row_dict['AVE_PRICE_STICK']['value']
                            price_ratio = comp_price/own_price
                            row_dict[xvar]['value'] = price_ratio
                # Check if the xvar iterated is competitor own price ratio lags
                elif row_dict[xvar]['feature_type'].__eq__('lag price') and 'shop' not in xvar.split('_'):
                    lag_no = int(xvar.split('_')[3])
                    price_per_item = 0.0

                    if len(self._consolidated_data)>0:
                        price_per_item = self._consolidated_data.PRICE_PER_ITEM[0]
                        week_index = list(self._pricing_df.columns[5:]).index(week_date)

                        if week_index >= lag_no:
                            pricing_week = self._pricing_df.columns[5:][week_index - lag_no]
                            
                            pricing_mask = (self._pricing_df.PARENT_CATEGORY.isin([self._product_info_dict.get('PARENT')])) & \
                                        (self._pricing_df.PRODUCT_CATEGORY.isin([self._product_info_dict.get('CATEGORY')])) & \
                                        (self._pricing_df.PRODUCT.isin([self._product_info_dict.get('PRODUCT')])) & \
                                        (self._pricing_df.SHOP.isin([self._product_info_dict.get('SHOP')]))
                            pricing_data = self._pricing_df.loc[pricing_mask].reset_index(drop=True)
                            
                            if len(pricing_data)>0:
                                lagged_price = float(pricing_data[pricing_week][0])
                                row_dict[xvar]['value'] = lagged_price
                        else:
                            continue

            except Exception as ex:
                # self._logger.error('Modifying Pricing Ratios Caught Exception as: '+str(ex), exc_info=True)
                continue
        
        return row_dict

    def predict(self):
        """
        This method helps in predicting input data based on two methods. These are:
        1. Reading Pickle files and getting model predictions
        2. Requesting Model APIs and getting model predictions
        Parameters: 
            None
        Returns: 
            request status code (int): 200 fr success, 800 for failure and so
            predicted json (json): textual response from the API or pickle file under consideration
        """
        self._bearer_key = 'bearer key'
        if self._pickle_flag:
            return predict_fn(pkl=os.path.join('datasets', 'models_essentials_v02', self._model_pkl), 
                            data=self._final_data_dict)
        else:
            return predict_service(uri=self._model_uri, 
                                bearer_key=self._bearer_key,
                                json_dict={
                                    'data':self._final_data_dict['data'],
                                    'model':self._reg_model_name}
                                )

def predict_service(uri=None, bearer_key=None, json_dict=None):
    """
        This method helps in requesting Model APIs and getting model predictions
        Parameters: 
            uri (str): Model URI to request
            bearer_key (str): Access token for making the request to respective URI
            json_dict (dict, (list, float)): Generated Input Data for respective model 
        Returns: 
            request status code (int): 200 fr success, 800 for failure and so
            predicted json (json): textual response from the API or pickle file under consideration
    """
    if uri is None or bearer_key is None or json_dict is None:
        print('Not a Standard request')
        return

    # URL for the web service
    scoring_uri = uri
    # If the service is authenticated, set the key or token
    api_key = bearer_key
    # Convert to JSON string
    input_data = json.dumps(json_dict)

    # Set the content type
    headers = {'Content-Type': 'application/json'}
    # If authentication is enabled, set the authorization header
    headers['Authorization'] = f'Bearer {api_key}'

    # Make the request and display the response
    response = requests.post(scoring_uri, input_data, headers=headers)
    return response.status_code, response.text

def predict_fn(pkl=None, data=None):
    """
        This method helps in loading respective pickle file and making the prediction
        Parameters: 
            pkl (str): Model Pickle Name
            data (dict, (list, float)): Generated Input Data for respective model 
        Returns: 
            request status code (int): 200 fr success, 800 for failure and so
            predicted json (json): textual response from the API or pickle file under consideration
    """
    if pkl is None or data is None:
        print('Not a Standard operation')
        return
    
    # Load respective model from pkl file
    model = None
    with open(pkl,'rb') as pkl_file:
        model = pickle.load(pkl_file)

    # Hit the predict function and return the response
    try:
        predictions = model.predict(data['data'])
        return 200, ','.join(str(x) for x in predictions)
    except Exception as ex:
        return 400, str(ex)
