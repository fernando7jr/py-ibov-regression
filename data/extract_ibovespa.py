#!/usr/bin/env python
'''Extract the daily B3 index data to a csv file
IBOVESPA Data source: http://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-estatisticas-historicas.htm
'''

from base64 import encodebytes
import csv
import datetime
import json
import requests
from os import path
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SAVE_DIR = path.dirname(path.realpath(__file__))


import requests
from base64 import encodebytes


def fetch_index_data(year, index='IBOVESPA', language='pt-br'):
    data = json.dumps({'year': year, 'index': index, 'language': language}).encode()
    payload = encodebytes(data).decode().rstrip()
    response = requests.get(
        f'https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/{payload}',
        verify=False
    )
    assert response.status_code == 200, f'Invalid response:\n{response.text}'
    return response.json()


def process_index_year(year, index):
    results = fetch_index_data(year, index)['results']
    for result in results:
        day = result['day']
        months = [
            result['rateValue1'],
            result['rateValue2'],
            result['rateValue3'],
            result['rateValue4'],
            result['rateValue5'],
            result['rateValue6'],
            result['rateValue7'],
            result['rateValue8'],
            result['rateValue9'],
            result['rateValue10'],
            result['rateValue11'],
            result['rateValue12'],
        ]
        for month in range(len(months)):
            value = months[month]
            if value is None:
                continue
            date = datetime.datetime(year=year, month=month + 1, day=day).strftime('%Y-%m-%d')
            yield date, float(value.replace('.', '').replace(',', '.'))


def save_index_data(outdir=SAVE_DIR, index='IBOVESPA', outfilename='{index}.csv'):
    index = str(index) if index else 'IBOVESPA'
    outfilename = (str(outfilename) if outfilename is not None else '{index}.csv').format(index=index.lower())
    outpath = path.join(outdir, outfilename)
    print(f'Extracting {index} to "{outpath}"')
    with open(outpath, 'wt') as f:
        csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['date', 'value'])
        for year in range(1998, datetime.date.today().year + 1):
            print(f'\t{index}: year {year}')
            csv_writer.writerows(process_index_year(year, index))
    return outpath


if __name__ == '__main__':
    save_index_data()
