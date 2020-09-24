import requests
import pandas as pd


#Chama a api para pegar a listagem de todas as moedas com suas cotacoes
def gera_dataframe_moedas_cotacao(dia,mes,ano):

	#faz requisição para a API do Banco Central através de um endereço que retorna um arquivo com todas as cotações(Sem BRL e USD)
    #Usando valor de endereço de teste e pegando seu csv e adicionando em um dataframe de pandas
    df_csv_moedas=pd.read_csv("https://www4.bcb.gov.br/Download/fechamento/20200923.csv",sep=';',header=None)
    
    #Printa os valores das colunas para teste
    print(df_csv_moedas.keys())
    for column in df_csv_moedas:
        print(df_csv_moedas[column])    
        '''for line in c[column]:
            print(line)
            print("\n"  )'''



gera_dataframe_moedas_cotacao(1,1,1)