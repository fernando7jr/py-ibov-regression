#!/usr/bin/env python
"""Extract the daily USD/BRL exchange data to a csv file
Data source: http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M
"""

from bs4 import BeautifulSoup
import csv
import datetime
import requests
from os import path


SAVE_DIR = path.dirname(path.realpath(__file__))


def fetch_dollar_data():
    response = requests.get('http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M')
    assert response.status_code == 200, f'Invalid response:\n{response.text}'
    return response.text


def __map_row(date, value):
    return (
        datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d'), 
        float(value.replace(',', '.'))
    )


def process_dollar_data():
    raw_html = fetch_dollar_data()
    html = BeautifulSoup(raw_html, features='html.parser')
    rows = html.select('#grd_DXMainTable > tr:not(:first-child)')
    return (
        __map_row(*row.get_text(separator=';', strip=True).split(';'))
        for row in rows
    )


def save_dollar_data(outdir=SAVE_DIR, outfilename='dollar.csv'):
    outfilename = str(outfilename) if outfilename is not None else 'dollar.csv'
    outpath = path.join(outdir, outfilename)
    print(f'Extracting DailyDollar to "{outpath}"')
    with open(outpath, 'wt') as f:
        csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['date', 'value'])
        csv_writer.writerows(process_dollar_data())
    return outpath


if __name__ == '__main__':
    save_dollar_data()
