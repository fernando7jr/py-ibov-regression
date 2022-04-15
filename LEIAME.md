# Regressão do IBOV por Machine Learning

Esse projeto é um trabalho de machine learning utilizando a linguagem python com sklearn.
O objetivo desse trabalho é gerar um modelo que por regressão faça a predição do [índice IBOV (IBOVESPA)](https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/ibovespa.htm).

## Primeiros passos

O projeto requer que a lingaugem Python 3 esteja instalada para executar os scripts.

* Clone o projeto
* Execute `pip install -r requirements.txt` para instalar as dependências.
* Execute `python -m data` para fazer a extração e preparo dos dados. Todos os arquivos são armazenados no formato csv dentro do diretório `data`.
* Execute `python model.py` para treinar e medir o desempenho dos modelos. O melhor deles será armazenado como `model.bin` pela biblioteca `pickle`. Por hora apenas o SVR é considerado na escolha.

## Uso

O script tentará diferentes algoritmos e colunas de dados. Toda a análise de performance e os gráficos gerados são exibidos durante o processo.
O modelo pode ser carregado em memória a qualquer momento a partir do arquivo `model.bin`. Ele pode ser reutilizado em diferentes apicaçõs, mas dependendo da modelagem talvez seja necessário normalizar os dados antes de usa-lo.
Para personalizar o processo de modelagem edite o arquivo `config.json` dentro do diretório `data`.

### Built-in script

O repositório vem com script pronto para usar o modelo selecionado. Ele já trata todas as normalizações necessárias além de "traduzir" a saída do modelo para o formato de pontos.
Siga as instruções do projeto antes de usar. É necessário já ter os dados armazenado além do arquivo `model.bin`.
O script bem pronto apenas para a váriavel de data por enquanto, já que os melhores modelos apenas utilizam ela.

## Lincença

Esse projeto é open-source e fruto de pesquisa acadêmica. Não há qualquer guarantia de que as predições tragam algum resultado.
Para mais informações leia a [lincensa de uso](https://github.com/fernando7jr/py-ibov-regression/blob/master/LICENSE).
