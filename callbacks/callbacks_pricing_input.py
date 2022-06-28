__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

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
    print('df consolidated : ', df_consolidated.columns.unique())
    if period_type.__eq__('Quarterly'):
        RSP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=st_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=st_month2week_list)])
    elif period_type.__eq__('Annually'):
        RSP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=lt_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=lt_month2week_list)])
    elif period_type.__eq__('Custom'):
        cdr_month_range, cdr_week_range = custom_datepicker(start_date=custom_start_date, end_date=custom_end_date)
        RSP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=cdr_month_range)])
        TMP_structure = pd.concat([df_consolidated[['PROVINCE','MANUF','BRAND','KA','PRICE_PACK_13W','PRICE_PACK_4W','PRICE_PACK_LATEST']],pd.DataFrame(columns=cdr_week_range)])