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
        self._product_info_dict = kwargs.get('product_info_dict') # Stores Info about products for which simulation needs to be fired
        self._month_to_weeks = kwargs.get('month_to_weeks') # Month to Week Mapping
        self._pickle_flag = kwargs.get('pickle_flag') # Model to predict from pickle files or model endpoints
        self._logger = kwargs.get('logger') # Logger Object for logging operational steps
        
        '''
        self._model_uri, self._bearer_key, self._reg_model_name = self.map_model_endpoint() # Extracts Model URL for respective Province + Brand Combination
        self._model_pkl = self.map_model_picklefile() # Extracts Name of Pickle file for respective Province + Brand Combination
        self._model_comp = self.map_model_comp() # Extracts competitor rank data based on Province + Brand i.e. irrespective of KA it is constant 
        self._features_dict = self.map_features() # Extracts Significant features for the respective Province + Brand Combination in a dictionary with latest values
        self._combined_own_df, self._combined_comp_df = self.split_historic_df() # Extracts Own and Competitor Consolidate Price Per Stick
        '''
        
        self._final_data_dict = {'data':[]} 