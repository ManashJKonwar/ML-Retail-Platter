__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
import json
import pickle

def generate_model_map(**kwargs):
    """
    This method generates teh mapping for each parent category
    Parameters: 
        kwargs : Multiple Arguments
            config_file_path (str): configuration file path
            model_file_path (str): directory path in which all model files are being stored
            model_mapper_file (pickle): pickle files which stores the id mapping for parent product category
    Returns: 
        None
    """
    config_file_path = kwargs.get('config_file_path')
    model_file_path = kwargs.get('model_file_path')
    model_mapper_file = kwargs.get('model_mapper_file')

    if not os.path.exists(config_file_path):
        # Model file 
        model_list=[]
        for file in os.listdir(model_file_path):
            if file.endswith(".pkl") and file.startswith("model"):
                model_list.append(file)
        print(model_list)
        
        # Read mapper file
        parent_category_dict = {}
        with open(model_mapper_file, 'rb') as mapper_file:
            parent_category_dict = pickle.load(mapper_file)
        
        # Mapper utility
        parent_model_dict = {}
        for parent_cat in parent_category_dict:
            print(parent_cat)
            parent_cat_index = parent_category_dict.get(parent_cat)

            for model_file in model_list:
                if str(parent_cat_index) == model_file.split('_')[2]:
                    parent_model_dict[parent_cat] = model_file
                    break

        # Saving the mapper config file
        with open(config_file_path, 'w', encoding='ascii') as model_config_file:
            json.dump(parent_model_dict, model_config_file, indent=4) 

if __name__ == '__main__':
    generate_model_map(
        config_file_path=os.path.join('config','config_modelpicklefiles.json'),
        model_file_path=os.path.join('datasets','models_essentials_v02'),
        model_mapper_file=os.path.join('datasets','models_essentials_v02','parent_cat_map.pkl')
    )