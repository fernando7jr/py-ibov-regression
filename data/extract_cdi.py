#!/usr/bin/env python
"""Extract the daily CDI and SELIC data to a csv file
Data source: http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v05_template_informacoes_di.asp?str_Modulo=completo&int_Idioma=1&int_Titulo=6&int_NivelBD=2
"""

from bs4 import BeautifulSoup
from csv import QUOTE_NONNUMERIC
import datetime
from io import StringIO
from os import path
import pandas as pd
import requests
from urllib.parse import urlencode
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


SAVE_DIR = path.dirname(path.realpath(__file__))
URL_BASE = 'http://estatisticas.cetip.com.br/astec'
TODAY = datetime.date.today()


def __get_csv():
    year, month, day = str(TODAY.year), str(
        TODAY.month).zfill(2), str(TODAY.day).zfill(2)
    session = requests.Session()

    response = session.post(
        f'{URL_BASE}/series_v05/paginas/lum_web_v04_10_02_gerador_sql.asp',
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://estatisticas.cetip.com.br',
            'Cache-Control': 'max-age=0',
            'Referer': f'{URL_BASE}/lum_web_v05_template_informacoes_di.asp?str_Modulo=completo&int_Idioma=1&int_Titulo=6&int_NivelBD=2',
        },
        data=urlencode({
            'DT_DIA_DE': '01',
            'DT_MES_DE': '01',
            'DT_ANO_DE': '1998',
            'DT_DIA_ATE': day,
            'DT_MES_ATE': month,
            'DT_ANO_ATE': year,
            'str_TipoDescricao': '5',
            'str_TipoFaixaPrazo': '0',
            'str_NomeArquivo': 'WEB_00_DI_Taxas_Over',
            'str_NomeTabela': 'WEB_DI_Taxas_Over',
            'str_Ativo': 'DI',
            'str_ModeloDados': 'TAX_001di',
            'str_TipoEmissao': '0',
            'str_Descricao': '_Geral',
            'str_Populacao': '_Geral',
            'str_FaixaPrazo': '_Geral',
            'str_NrLeilao': '_Geral',
            'str_ModeloLeilao': '_Geral',
            'str_FaixaPrazoTotalizado': '0',
            'str_Emissao': '_Geral',
            'str_ApresentarTipoOp': '0',
            'str_Observacao': '!DI-CETIP (over)||Observacoes a respeito de mudanca de moeda / volume',
            'str_NomeAtivoCabecalho': 'DI - Depósito Interfinanceiro',
            'str_NomeTipoInformacaoCabecalho': 'Taxas - DI PRÉ - Over',
            'int_Idioma': '1',
        }),
        verify=False
    )

    assert response.status_code == 200, f'Invalid response:\n{response.text}'
    html = BeautifulSoup(response.text, features='html.parser')
    response = session.post(
        f'{URL_BASE}/series_v05/paginas/lum_web_v04_10_03_consulta.asp',
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://estatisticas.cetip.com.br',
            'Cache-Control': 'max-age=0',
        },
        data=urlencode({
            _input.attrs['name']: _input.attrs['value']
            for _input in html.select('input[type="hidden"]')
        }),
        verify=False
    )

    assert response.status_code == 200, f'Invalid response:\n{response.text}'
    html = BeautifulSoup(response.text, features='html.parser')
    form_input = html.select_one('input[name="str_ArquivoExcel"]')
    assert form_input is not None, 'Failed to find input[name="str_ArquivoExcel"]'
    file_name = form_input.attrs['value']

    response = session.get(
        f'{URL_BASE}/temp/{file_name}',
        headers={
            'Host': 'estatisticas.cetip.com.br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Referer': 'http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v04_10_03_consulta.asp',
        }
    )
    assert response.status_code == 200, f'Invalid response:\n{response.text}'
    return StringIO(response.text)


def process_cdi_data():
    return pd.read_csv(
        __get_csv(),
        sep='\t',
        skiprows=10,
        names=['date', 'nr_op', 'volume', 'mean', 'daily_factor',
               'min', 'max', 'mode', 'std_dev', 'selic'],
        parse_dates=[0],
        date_parser=lambda d: datetime.datetime.strptime(d, '%d/%m/%Y'),
        decimal=',',
        thousands='.',
        encoding="windows-1252",
    )


def save_cdi_data(outdir=SAVE_DIR, outfilename='cdi.csv'):
    outfilename = str(outfilename) if outfilename is not None else 'cdi.csv'
    outpath = path.join(outdir, outfilename)
    print(f'Extracting DailyCDI to "{outpath}"')
    df = process_cdi_data()
    df.to_csv(
        outpath,
        decimal='.',
        sep=',',
        index=False,
        columns=['date', 'mean', 'selic'],
        header=['date', 'cdi', 'selic'],
        quoting=QUOTE_NONNUMERIC
    )
    return outpath


if __name__ == '__main__':
    save_cdi_data()
