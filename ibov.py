import pandas as pd
import pickle
from data import DATA_FILENAME, to_days_since_1998, datetime


def parse_date(string_value: str) -> int:
    try:
        return datetime.datetime.strptime(string_value.strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


COLUMNS = ['ibovespa']
df = pd.read_csv(DATA_FILENAME, usecols=COLUMNS)
max_values = {
    col: df[col].max()
    for col in COLUMNS
}
df = None


MODELS = {
    'date': {
        'transform': parse_date, 
        'normalize': to_days_since_1998, 
        'file': 'svr_model.bin',
        'input_label': 'Entre com a data (DD/MM/YYYY): ',
        'error_label': 'A data informada não é valida! Por favor tente novamente...'
    }, 
}


print('''Esse programa não garante o seus resultados e não se responsabiliza pelo mesmos.
O modelo utilizado é fruto de um projeto de pesquisa com fins acadêmicos. Todo o projeto está disponível em: https://github.com/fernando7jr/py-ibov-regression
Funcionamento:
  * Informe a data no formato DD/MM/YYYY.
  * O programa calcula com base no modelo de aprendizado de máquina qual a pontuação possível de acordo com os paramêtros informados.

Pressione ^Z (CTRL+Z) ou ^C (CTRL+C) para sair a qualquer momento.

''')

model_config = MODELS['date']

# load the model
f = open(model_config['file'], 'rb')
model = pickle.load(f)
f.close()

while True:
    value = input(model_config['input_label'])
    value = model_config['transform'](value)
    if value is None:
        print(model_config['error_label'])
        continue
    value_norm = model_config['normalize'](value)

    X = [[value_norm]]
    y = model.predict(X)
    ibov = max_values['ibovespa'] * y[0]
    print(f'De acordo com o modelo, o valor esperado paro IBOV é de {str(ibov).replace(".", ".")} pontos\n')
