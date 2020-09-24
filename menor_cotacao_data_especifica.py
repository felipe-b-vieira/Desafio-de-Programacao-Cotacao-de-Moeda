import requests
import pandas as pd


#Chama a api para pegar a listagem de todas as moedas com suas cotacoes
def gera_dataframe_moedas_cotacao(dia,mes,ano):
	#faz requisição para a API do Banco Central através de um endereço que retorna um arquivo com todas as cotações(Sem BRL e USD)
    #Usando valor de endereço de teste e pegando seu csv e adicionando em um dataframe de pandas
    df_csv_moedas=pd.read_csv("https://www4.bcb.gov.br/Download/fechamento/20200923.csv",sep=';',header=None,names=["#","Cod Moeda","Tipo","Moeda","Taxa Compra","Taxa Venda","Paridade Compra","Paridade Venda"])
    return df_csv_moedas


def calcular_dolar_df(df):
    #itera sobre cada linha do Dataframe para calcular o valor do dólar com base no cálculo passado pelo site(Depende do tipo de Moeda)
    valores_dolar=[]
    for index, row in df.iterrows():
        if(row["Tipo"]=="A"):
            valores_dolar.append(1/float(row["Paridade Compra"].replace(',','.')))
        elif(row["Tipo"]=="B"):
            valores_dolar.append(1*float(row["Paridade Compra"].replace(',','.')))
        else:
            valores_dolar.append(-1)
    df["Valor_dolar"] = valores_dolar
    return df



def acha_menor_valor_dolar(df):
    
    #acha o menor valor de dolar na linha de valores do dólar
    #pos_valores_minimos_df = df.idxmin()
    print(df["Valor_dolar"])


df_moedas_cotacao = gera_dataframe_moedas_cotacao(1,1,1)
df_moedas_cotacao = calcular_dolar_df(df_moedas_cotacao)
acha_menor_valor_dolar(df_moedas_cotacao)