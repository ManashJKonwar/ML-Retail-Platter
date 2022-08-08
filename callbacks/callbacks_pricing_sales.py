__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash.dependencies import Input, Output, State
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
        if prediction_value_type.__eq__('Count'):
            df_intermediate = df_predicted.copy()
            # Converting string based predicted values to float column type
            for colname in df_intermediate.columns[3:]:
                try:
                    df_intermediate[colname] = df_intermediate[colname].astype(float)
                    df_intermediate[colname] = df_intermediate[colname].apply(lambda x:x/1)
                except Exception:
                    continue
            # Round off intermediate dataframe
            df_intermediate = df_intermediate.round(0)
            # Assign df_predicted 
            df_predicted = df_intermediate
        elif prediction_value_type.__eq__('Share_by_Count'):
            df_intermediate = df_predicted.copy()
            # Converting string based predicted values to float column type
            # Dividing each column value by sum of the column
            for colname in df_intermediate.columns[3:]:
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
            for colname in df_predicted.columns[3:]:
                try:
                    df_intermediate[colname] = df_intermediate[colname].astype(float)
                    df_pricing[colname] = df_pricing[colname].astype(float)
                    df_intermediate[colname] = df_intermediate[colname] * df_pricing[colname], 
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

# Download Device Sales Data to CSV
@callback_manager.callback(Output(component_id='download-sales-csv', component_property='data'),
                        Input(component_id='btn-download-sales', component_property='n_clicks'),
                        State(component_id='datatable-output', component_property='data'), prevent_initial_call=True)
def sales_download_link(on_click, sales_data):
    if on_click is not None and sales_data is not None:
        oritemplate = pd.DataFrame(data = sales_data)
        return dcc.send_data_frame(oritemplate.to_csv, "predicted_sales.csv", index=False)
#endregion

# Setting up options and dropdown value for Predicted Category Dropdown
@callback_manager.callback([Output(component_id='dd-category-predicted', component_property='options'),
                        Output(component_id='dd-category-predicted', component_property='value')],
                        Input(component_id='storage-pricing-output', component_property='data'))
def update_predicted_province_options(stored_sales_prediction):
    if stored_sales_prediction is not None:
        # Extract Simulated category
        category_selection_list = []
        try:
            sales_df = pd.DataFrame(stored_sales_prediction).copy()
            category_selection_list = sales_df.PRODUCT_CATEGORY.unique().tolist()
        except Exception:
            pass
        options = [{'label': i, 'value': i} for i in category_selection_list]
        return options, category_selection_list[0]
    else:
        return dash.no_update, dash.no_update

# Setting up options and dropdown value for Predicted Shop Dropdown
@callback_manager.callback([Output(component_id='dd-shop-predicted', component_property='options'),
                        Output(component_id='dd-shop-predicted', component_property='value')],
                        [Input(component_id='storage-pricing-output', component_property='data'),
                        Input(component_id='dd-category-predicted', component_property='value')])
def update_predicted_brand_options(stored_sales_prediction, dd_category_value):
    if stored_sales_prediction is not None and dd_category_value is not None:
        # Extract Simulated Shop
        shop_selection_list = []
        try:
            sales_df = pd.DataFrame(stored_sales_prediction).copy()
            category_mask = sales_df.PRODUCT_CATEGORY.isin([dd_category_value])
            sales_df = sales_df.loc[category_mask]
            shop_selection_list = sales_df.SHOP.unique().tolist()
        except Exception:
            pass
        options = [{'label': i, 'value': i} for i in shop_selection_list]
        return options, shop_selection_list[0]
    else:
        return dash.no_update, dash.no_update

# Sales Charting based on Category and Shop Selected
@callback_manager.callback(Output(component_id='g-sales', component_property='figure'),
                        [Input(component_id='storage-pricing-output', component_property='data'),
                        Input(component_id='dd-category-predicted', component_property='value'),
                        Input(component_id='dd-shop-predicted', component_property='value')])
def sales_predicted_charting(stored_sales_prediction, dd_category_value, dd_shop_value):
    tracer_list=[]
    if stored_sales_prediction is not None and len(stored_sales_prediction)>0 and\
    dd_category_value is not None and dd_shop_value is not None:
        df_predicted = pd.DataFrame(stored_sales_prediction).copy()
        # Filter based on Province and Brands Selected
        selection_mask = ((df_predicted.PRODUCT_CATEGORY.isin([dd_category_value])) & (df_predicted.SHOP.isin(dd_shop_value))) if isinstance(dd_shop_value, list) else \
                        ((df_predicted.PRODUCT_CATEGORY.isin([dd_category_value])) & (df_predicted.SHOP.isin([dd_shop_value])))
        df_predicted = df_predicted.loc[selection_mask].reset_index(drop=True)

        df_intermediate = df_predicted.copy()
        df_intermediate = df_intermediate.T

        stacked_counter=0
        for product in df_predicted['PRODUCT']:
            try:
                tracer = go.Bar(x=df_intermediate[3:].index, y=df_intermediate[stacked_counter][3:], name=product)
                tracer_list.append(tracer)
            except Exception as ex:
                print(ex)
                continue
            finally:
                stacked_counter+=1

        figure={
            'data':tracer_list,
            'layout':go.Layout(title='Predicted Volume Sales', barmode='stack')
        }
        return figure
    else:
        return dash.no_update