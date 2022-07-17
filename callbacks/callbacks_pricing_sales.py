__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash
from callback_manager import CallbackManager

callback_manager = CallbackManager()

@callback_manager.callback([Output(component_id='datatable-output', component_property='data'),
                        Output(component_id='datatable-output', component_property='columns')],
                        [Input(component_id='storage-pricing-output', component_property='data'),
                        Input(component_id='radioitem-prediction', component_property='value')],
                        State(component_id='storage-pricing-input', component_property='data'))
def sales_output(stored_sales_prediction, prediction_value_type, stored_pricing_data):
    if stored_sales_prediction is not None:
        df_predicted = pd.DataFrame(stored_sales_prediction)
        
        # Modifying Predicted Data to fulfil the representation type 
        if prediction_value_type.__eq__('Sticks'):
            df_intermediate = df_predicted.copy()
            # Converting string based predicted values to float column type
            # Dividing each column value by 1000 so as to express predictions per 1000 sticks
            for colname in df_intermediate.columns[3:]:
                try:
                    df_intermediate[colname] = df_intermediate[colname].astype(float)
                    # df_intermediate[colname] = df_intermediate[colname].apply(lambda x:x/1000)
                    df_intermediate[colname] = df_intermediate[colname].apply(lambda x:x/1)
                except Exception:
                    continue
            # Round off intermediate dataframe
            df_intermediate = df_intermediate.round(0)
            # Assign df_predicted 
            df_predicted = df_intermediate
        elif prediction_value_type.__eq__('Share'):
            df_intermediate = df_predicted.copy()
            # Converting string based predicted values to float column type
            # Dividing each column value by sum of the column
            for colname in df_intermediate.columns[4:]:
                try:
                    df_intermediate[colname] = df_intermediate[colname].astype(float)
                    df_intermediate[colname] = (df_intermediate[colname]/df_intermediate[colname].sum()) * 100
                except Exception:
                    continue
            # Round off intermediate dataframe
            df_intermediate = df_intermediate.round(4)
            # Assign df_predicted 
            df_predicted = df_intermediate
        elif prediction_value_type.__eq__('Value'):
            df_pricing = pd.DataFrame(stored_pricing_data)
            df_intermediate = df_predicted.copy()
            for colname in df_predicted.columns[4:]:
                try:
                    df_intermediate[colname] = df_intermediate[colname].astype(float)
                    df_pricing[colname] = df_pricing[colname].astype(float)
                    df_intermediate[colname] = np.where((df_intermediate['PROVINCE'] == 'BRITISHCOLUMBIA') | (df_intermediate['PROVINCE'] == 'NEWFOUNDLAND&LABR.'), \
                                                    (df_intermediate[colname]*1000) * (df_pricing[colname]/20) / 100, 
                                                    (df_intermediate[colname]*1000) * (df_pricing[colname]/25) / 100)
                except Exception:
                    continue
            # Round off intermediate dataframe
            df_intermediate = df_intermediate.round(4)
            # Assign df_predicted 
            df_predicted = df_intermediate

        column_list = []
        for column_name in df_predicted.columns:
            column_list.append({"name": column_name, "id": column_name})
        return df_predicted.to_dict('records'), column_list
    else:
        return dash.no_update, dash.no_update