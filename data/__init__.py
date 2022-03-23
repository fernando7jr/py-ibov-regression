from .extract_cdi import save_cdi_data
from .extract_dollar import save_dollar_data
from .extract_ibovespa import save_index_data

from os import path

SAVE_DIR = path.dirname(path.realpath(__file__))
DATA_FILENAME = path.join(SAVE_DIR, 'data.csv')
MODEL_CONFIG_FILENAME = path.join(SAVE_DIR, 'config.json')

def load_model_config():
    import json

    with open(MODEL_CONFIG_FILENAME, 'r') as f:
        config = json.load(f)
    return config
