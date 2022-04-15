# IBOV Regression through Machine Learning

This is a machine learning project using python and sklearn.
The goal of the project is to use regression to predict the [IBOV index (Sao Paulo stock market index)](https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/ibovespa.htm).

\* Para português clique [aqui](https://github.com/fernando7jr/py-ibov-regression/blob/master/LEIAME.md). (Portuguese language version)

## Setup

Python 3 is required in order to run the scripts.

* Clone the project
* Run `pip install -r requirements.txt` to install the libraries.
* Run `python -m data` in order to scrap and prepare all the required data. All files are stored in csv format in the `data` folder.
* Run `python model.py` to train and evaluate the models. The best one will be saved as `model.bin` by `pickle`. For now only SVR will be considered.

## Usage

The script will try different estimators and features. The whole evaluation along the generated charts will be outputed during the process.
The model can be reloaded from its binary file at any time and reused for different applications. Please note that data can be normalized depending of the selected columns.
In order to customise the modeling process, edit the file `config.json` inside the `data` folder.

### Built-in script

A built-in script is provided with the project to use the selected model. It will do all the required normalization and translate the output back to the index "points" format. 
Please follow the setup before using it. Also bear in mind that the cli is in Portuguese language only and it only handles the date inputs. Although it is easy to extend it.

## Disclaimer

This is just an academic research and by no means I guarantee the correctness of the predctions. Use at your own risk.
The repository is published with a open-source license. Please check it [here](https://github.com/fernando7jr/py-ibov-regression/blob/master/LICENSE) for more information.
