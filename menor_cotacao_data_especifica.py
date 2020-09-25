import requests
import pandas as pd
from bs4 import BeautifulSoup
from decimal import Decimal
from math import inf

# CONSTANTES
MONTANTE = 1
NOTACAO_CIENTIFICA = False
POSICAO_NOME_PAIS = 4
POSICAO_CODIGO_PAIS = 0
QUANTIDADE_MINIMA_CELULAS = 4


# Chama a api para pegar a listagem de todas as moedas com suas cotações
def gera_dataframe_moedas_cotacao(data):
    # Faz requisição para a API do BCB através de um endereço que retorna um csv com as cotações (Sem BRL e USD)
    # Usando valor de endereço de teste e pegando seu csv e adicionando em um dataframe de pandas
    # O Csv não tem header, precisa adicionar manualmente(Iguais ao site)
    df_csv_moedas = pd.read_csv("https://www4.bcb.gov.br/Download/fechamento/" + data + ".csv", sep=';',
                                header=None, names=["#", "Cod Moeda", "Tipo", "Moeda", "Taxa Compra", "Taxa Venda",
                                                    "Paridade Compra", "Paridade Venda"])
    return df_csv_moedas


def calcular_dolar_df(df_moedas):
    # itera sobre cada linha do Dataframe para calcular o valor do dólar com base no seu tipo
    valores_dolar = []
    for indice, infos_moeda in df_moedas.iterrows():
        # Usa paridade de compra para mostrar o valor de dólar da moeda
        paridade_moeda = float(infos_moeda["Paridade Compra"].replace(',', '.'))

        if (infos_moeda["Tipo"] == "A"):
            # Divide pela paridade
            valores_dolar.append(MONTANTE / paridade_moeda)
        elif (infos_moeda["Tipo"] == "B"):
            # Multiplica pela paridade
            valores_dolar.append(MONTANTE * paridade_moeda)
        else:
            # Valor arbitrário infinito para o caso de ter um tipo diferente dos apresentados
            valores_dolar.append(inf)

    df_moedas["Valor_dolar"] = valores_dolar
    return df_moedas


# Para manter o desafio em português, foi necessário realizar web scrapping para pegar os nomes
def gera_listagem_nomes_pais():
    # Utiliza o link da Wikipedia que lista os países que usam cada moeda
    url_codigos = "https://pt.wikipedia.org/wiki/ISO_4217"
    resposta_wikipedia = requests.get(url_codigos)

    # transforma em soup com parser html do beautifulsoup e recupera a tabela com os nomes dos paises
    soup_listagem_paises = BeautifulSoup(resposta_wikipedia.content, 'html.parser')
    tabela_paises = soup_listagem_paises.find('table', {"class": "wikitable sortable"})

    dict_paises = {}
    # Pega cada linha da tabela
    for linha_paises in tabela_paises.findChildren(['tr']):
        # Pega as células de cada linha, a primeira é o código e a última é o nome do país
        celulas_paises = linha_paises.findChildren(['td'])
        # Verifica se tem a quantidade mínima de células para ser um país
        if (len(celulas_paises) >= QUANTIDADE_MINIMA_CELULAS):
            # Seleciona o código do país(Primeira célula)
            codigo_pais = celulas_paises[POSICAO_CODIGO_PAIS].string
            # Verifica todos os links na quinta célula para encontrar o nome de todos os países
            nomes_paises = []
            ahref_nomes_paises = celulas_paises[POSICAO_NOME_PAIS].findAll(['a'])
            for nome_pais in ahref_nomes_paises:
                nomes_paises.append(nome_pais.string)
            # Salva o código como chave de um dicionário com seu valor sendo um array dos paises
            dict_paises[codigo_pais] = nomes_paises
    return dict_paises


def acha_infos_menor_dolar(df_moedas):
    # Pega a linha do dataframe de moedas que tenha o menor valor do dólar
    menor_moeda = df_moedas[df_moedas["Valor_dolar"] == df_moedas["Valor_dolar"].min()]

    # Pega o valor desejado, usando iloc para pegar o único valor e seu conteúdo
    simbolo_moeda = menor_moeda["Moeda"].iloc(0)[0]
    cotacao_moeda = menor_moeda["Valor_dolar"].iloc(0)[0]
    # Utiliza web scrapping para pegar listagem de nome do país em português
    dict_paises = gera_listagem_nomes_pais()
    # Usa o dicionario dos países para pegar a listagem de países dado o símbolo da moeda
    paises_moeda = dict_paises[simbolo_moeda]

    return simbolo_moeda, paises_moeda, cotacao_moeda


def retorna_resultado_menor_cotacao(simbolo_moeda, paises_moeda, cotacao_moeda):
    # printa as saidas
    print(simbolo_moeda, end=',')
    # Printa os nomes dos países
    for pais in paises_moeda:
        print(pais, end=',')
    # Usado para printar sem notacao cientifica
    if (NOTACAO_CIENTIFICA):
        print(cotacao_moeda)
    else:
        print(Decimal.from_float(cotacao_moeda))


# Lê a data no formato YYYYMMDD e retorna formatado para leitura de arquivo
def leitura_data():
    data_nao_formatada = input("Entre com a data no formato YYYYMMDD:\n")
    data_formatada = data_nao_formatada.strip("/")
    data_formatada = data_formatada.strip(" ")
    return data_formatada


# Função principal para uso com try except, retorna se encontrou um erro
def main_menor_cotacao():
    # Leitura da data e formatação para padrão da função
    data_moeda = leitura_data()
    # Tenta pegar o arquivo de cotação das moedas, se não conseguir, levanta exceção
    try:
        df_moedas_cotacao = gera_dataframe_moedas_cotacao(data_moeda)
    except Exception as e:
        print('x')
        return
    # Restante da função, calcula o valor em dólar das moedas e encontra o valor da moeda com menor valor
    df_moedas_cotacao = calcular_dolar_df(df_moedas_cotacao)
    simbolo, paises, cotacao = acha_infos_menor_dolar(df_moedas_cotacao)
    retorna_resultado_menor_cotacao(simbolo, paises, cotacao)


# Main do código, chama a função principal que faz a leitura das informações das moedas e encontra a menor cotação
if __name__ == "__main__":
    main_menor_cotacao()
