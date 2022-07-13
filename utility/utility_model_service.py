__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

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
        self._model_pkl = self.map_model_picklefile() # Extracts Name of Pickle file for respective Province + Brand Combination
        self._model_comp = self.map_model_comp() # Extracts competitor rank data based on Province + Brand i.e. irrespective of KA it is constant 
        self._combined_own_df, self._combined_comp_df = self.split_historic_df() # Extracts Own and Competitor Consolidate Price Per Stick
        '''
        self._features_dict = self._map_features() # Extracts Significant features for the respective Province + Brand Combination in a dictionary with latest values

        self._final_data_dict = {'data':[]} 

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
            '''
            # Masking features related to only specific Province and Brand from features dataframe
            feature_extraction_mask = (self._features_df.PROVINCE==self._province_brand_dict['PROVINCE']) &\
                                    (self._features_df.BRAND_AGG==self._brand_mapper_dict[self._province_brand_dict['BRAND']])&\
                                    (self._features_df.KA_AGG==self._ka_mapper_dict[self._province_brand_dict['KA']])
            feature_data = self._features_df.loc[feature_extraction_mask].reset_index(drop=True)
            # Masking features based on selected model type for specific Province and Brand
            model_extraction_mask = (self._model_endpoints_df.MODEL_ID==('_%s_%s_%s')%(
                                                                                    re.sub(r"\s+", "", self._province_brand_dict['PROVINCE']), \
                                                                                    self._brand_mapper_dict[self._province_brand_dict['BRAND']],\
                                                                                    self._ka_mapper_dict[self._province_brand_dict['KA']]
                                                                                    )
                                    ) 
            model_df = self._model_endpoints_df.loc[model_extraction_mask].reset_index(drop=True)
            
            if len(model_df)==1:
                model_type = model_df.MODEL[0]
            else:
                pass
                    
            feature_data = feature_data.loc[feature_data.MODEL.isin([model_type])].reset_index(drop=True) 
            '''

            xvar_extraction_mask = (self._xvar_df.item_category_id.isin([self._mapping_dict['category'][self._product_info_dict['CATEGORY']]])) & \
                            (self._xvar_df.shop_id.isin([self._mapping_dict['shop'][self._product_info_dict['SHOP']]])) & \
                            (self._xvar_df.item_id.isin([self._mapping_dict['product'][self._product_info_dict['PRODUCT']]]))
            consolidated_data = self._xvar_df.loc[xvar_extraction_mask].drop_duplicates(keep=False).reset_index(drop=True)
            
            for row in self._features_df.itertuples():
                if row.feature_name not in feature_dict.keys():
                    feature_dict[row.feature_name] = {'value':float(consolidated_data[row.feature_name])}
            #self._logger.info('Feature Extraction Done Successfully')
            return feature_dict
        except Exception as ex:
            raise ex

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
            counter = 4
            column_name_list, row_data = self._row_info_data[0], self._row_info_data[1]
            for item in column_name_list[4:]:
                try:
                    data_dict[item] = float(eval("row_data._"+str(counter)))
                    counter+=1

                except Exception as ex:
                    counter+=1
                    continue
        elif period_type.__eq__('Annually'):
            # Plain Execution of Monthly Level Data Provided
            counter = 4
            column_name_list, row_data = self._row_info_data[0], self._row_info_data[1]
            month_map={}
            for item in column_name_list[4:]:
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
            # Overridding Price Per Stick Value
            if 'AVE_PRICE_STICK' in row_dict.keys():
                row_dict['AVE_PRICE_STICK']['value'] = float(data_dict[key])
            # Overridding Trend Variable by Dynamically Calculated Value
            if 'LINEARTREND' in row_dict.keys():
                key_date = datetime.datetime.strptime(key, '%Y-%b-%d').date()
                start_date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()
                row_dict['LINEARTREND']['value'] = abs(key_date-start_date).days + 1
            # Modifying Seasonality and Weather Data
            row_dict = self.modify_backend_xvars(row_dict=row_dict, week_date=key)
            # Modifying Pricing Ratios
            row_dict = self.modify_pricing_ratios(period_type=period_type, row_dict=row_dict, week_date=key)
            # Modifying Lag Features
            row_dict = self.modify_lag_features(period_type=period_type, row_dict=row_dict, week_date=key)
            # Modifying Log Features # This needs to be the ending step of modifying it since we were playing with absolute values
            # till now
            row_dict = self.modify_log_features(row_dict=row_dict)
            # Adding to final data dictionary
            self._final_data_dict['data'] += [[x['value'] for x in list(row_dict.values())]]
        
        # self._logger.info('Generating Input Data Done Successfully with data length: %s' %(str(len(self._final_data_dict['data']))))