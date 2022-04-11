import pandas as pd
import pickle
from data import DATA_FILENAME, to_days_since_1998, datetime


f = open('model.bin', 'rb')
model = pickle.load(f)
f.close()

df = pd.read_csv(DATA_FILENAME)
max_values = {
    col: df[col].max()
    for col in ('dollar', 'cdi', 'ibovespa')
}


def parse_float(string_value: str) -> float:
    try:
        return float(string_value.replace('R$', '').replace(',', '.').strip())
    except ValueError:
        return None

def parse_date(string_value: str) -> int:
    try:
        return datetime.datetime.strptime(string_value.strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


print('''Esse programa não garante o seus resultados e não se responsabiliza por seus resultados.
O modelo utilizado é fruto de um projeto de pesquisa com fins acadêmicos.
Funcionamento:
  * Informe o preço do dólar em reais (R$).
  * Informe a média do CDI.
  * Informe a data que você quer saber qual será a pontuação.
  * O programa calcula com base no modelo de aprendizado de máquina qual a pontuação possível de acordo com os paramêtros informados.

Pressione ^Z (CTRL+Z) ou ^C (CTRL+C) para sair a qualquer momento.''')
while True:
    dollar = parse_float(input('Entre com o preço de compra do dólar em reais: '))
    if dollar is None:
        print(f'Valor "{dollar}" não é valido para o dólar! Por favor tente novamente...')
        continue
    cdi = parse_float(input('Entre com o valor do CDI: '))
    if dollar is None:
        print(f'Valor "{dollar}" não é valido para o CDI! Por favor tente novamente...')
        continue
    date = parse_date(input('Entre com a data (DD/MM/YYYY): '))
    if date is None:
        print(f'A data "{dollar}" não é valida! Por favor tente novamente...')
        continue

    dollar_norm = dollar / max_values['dollar']
    cdi_norm = cdi / max_values['cdi']
    date_norm = to_days_since_1998(date)
    X = [[dollar_norm, cdi_norm, date_norm]]
    y = model.predict(X)
    ibov = max_values['ibovespa'] * y[0]
    print(f'De acordo com o modelo, o valor esperado paro IBOV é de {str(ibov).replace(".", ".")} pontos\n')
