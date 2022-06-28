__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
from dash.dependencies import Input, Output, State
from callback_manager import CallbackManager
from datasets.backend import df_consolidated, lt_month_range, lt_month2week_list, st_month_range, st_month2week_list
from utility.utility_data_transformation import custom_datepicker

callback_manager = CallbackManager()

@callback_manager.callback([Output(component_id='datatable-input', component_property='data'),
                            Output(component_id='datatable-input', component_property='columns')],
                            [Input(component_id='dd-period', component_property='value'),
                            Input(component_id='dpr-period', component_property='start_date'),
                            Input(component_id='dpr-period', component_property='end_date'),
                            Input(component_id='dd-product-category', component_property='value'),
                            Input(component_id='dd-product-name', component_property='value'),
                            Input(component_id='dd-shop-name', component_property='value'),
                            Input(component_id='upload-data', component_property='contents'),
                            Input(component_id='btn-reset-simulator', component_property='n_clicks')],
                            State(component_id='storage-pricing-input', component_property='data'))
def set_simulation_input_data(period_type, custom_start_date, custom_end_date, sel_product_category, sel_product, sel_shop, \
                                uploaded_content, n_reset_simulator, stored_pricing_input):
    # Generate Consolidated DF based on Category, Product and Shop selected
    if period_type.__eq__('Quarterly'):
        RSP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=st_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=st_month2week_list)])
    elif period_type.__eq__('Annually'):
        RSP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=lt_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=lt_month2week_list)])
    elif period_type.__eq__('Custom'):
        cdr_month_range, cdr_week_range = custom_datepicker(start_date=custom_start_date, end_date=custom_end_date)
        RSP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=cdr_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']],pd.DataFrame(columns=cdr_week_range)])

    # Check for None type province, ka, manufacturer, brand instance
    if sel_product_category is None or len(sel_product_category) == 0:
        sel_product_category = [product_cat for product_cat in df_consolidated.PRODUCT_CATEGORY]
    if sel_product is None or len(sel_product) == 0:
        sel_product = [product for product in df_consolidated.PRODUCT]
    if sel_shop is None or len(sel_shop) == 0:
        sel_shop = [shop for shop in df_consolidated.SHOP]

    # Table structure for RSP and TMP with default price across period rounded off to 3 decimals
    RSP_structure['PRICE_PER_ITEM'] = RSP_structure['PRICE_PER_ITEM'].map("{:.2f}".format)
    TMP_structure['PRICE_PER_ITEM'] = TMP_structure['PRICE_PER_ITEM'].map("{:.2f}".format)
    RSP_default = RSP_structure.ffill(axis = 1)
    TMP_default = TMP_structure.ffill(axis = 1)
    
    # Default structure
    if period_type.__eq__('Quarterly'):
        temp_default = TMP_default
    elif period_type.__eq__('Annually'):
        temp_default = RSP_default
    elif period_type.__eq__('Custom'):
        temp_default = TMP_default
    df_templatedata = temp_default.loc[temp_default.PRODUCT_CATEGORY.isin(sel_product_category)  & temp_default.PRODUCT.isin(sel_product) & temp_default.SHOP.isin(sel_shop), :]

    # Sorting Table with respect to combination of Province, Manuf and Brand
    df_templatedata = df_templatedata.sort_values(by=['PRODUCT_CATEGORY','PRODUCT','SHOP']).reset_index(drop=True)

    column_list = []
    for column_name in df_templatedata.columns:
        if column_name in ['PRODUCT_CATEGORY','PRODUCT','SHOP','PRICE_PER_ITEM']:
            column_list.append({"name": column_name, "id": column_name, 'editable': False})
        else:
            column_list.append({"name": column_name, "id": column_name})
    return df_templatedata.to_dict('records'), column_list