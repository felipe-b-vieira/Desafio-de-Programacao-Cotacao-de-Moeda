import requests
import pandas as pd
from bs4 import BeautifulSoup

#CONSTANTES
MONTANTE = 1


#Chama a api para pegar a listagem de todas as moedas com suas cotacoes
def gera_dataframe_moedas_cotacao(dia,mes,ano):
	#faz requisição para a API do Banco Central através de um endereço que retorna um arquivo com todas as cotações(Sem BRL e USD)
    #Usando valor de endereço de teste e pegando seu csv e adicionando em um dataframe de pandas
    #O Csv não tem header, preciso adicionar manualmente(Iguais ao site)
    df_csv_moedas=pd.read_csv("https://www4.bcb.gov.br/Download/fechamento/20200924.csv",sep=';',header=None,names=["#","Cod Moeda","Tipo","Moeda","Taxa Compra","Taxa Venda","Paridade Compra","Paridade Venda"])
    return df_csv_moedas


def calcular_dolar_df(df_moedas,MONTANTE):
    #itera sobre cada linha do Dataframe para calcular o valor do dólar com base no cálculo passado pelo site(Depende do tipo de Moeda)
    valores_dolar=[]
    for indice, infos_moeda in df_moedas.iterrows():
        #Usa paridade de compra para mostrar o valor de dólar da moeda
        paridade_moeda = float(infos_moeda["Paridade Compra"].replace(',','.'))
        
        if(infos_moeda["Tipo"]=="A"): 
            #Divide pela paridade
            valores_dolar.append(MONTANTE/paridade_moeda)
        elif(infos_moeda["Tipo"]=="B"): 
            #Multiplica pela paridade
            valores_dolar.append(MONTANTE*paridade_moeda)
        else:
            #Valor arbitrário negativo para o caso de ter um tipo diferente
            valores_dolar.append(-MONTANTE)
    
    df_moedas["Valor_dolar"] = valores_dolar
    return df_moedas
    
    
#Para mantar o trabalho todo em português, foi necessário realizar web scrapping para pegar os nomes dos países brasileiros com base no seu código
def gera_listagem_nomes_pais():
    #Utiliza o link da Wikipedia que lista os países que usam cada moeda
    URL_codigos = "https://pt.wikipedia.org/wiki/ISO_4217"
    resposta_wikipedia = requests.get(URL_codigos)

    #transforma em soup com parser html do beautifulsoup e recupero a tabela com os nomes do país
    soup_listagem_paises = BeautifulSoup(resposta_wikipedia.content, 'html.parser')
    tabela_paises = soup_listagem_paises.find('table',{"class":"wikitable sortable"})
    
    dict_paises = {}
    #pego cada linha da tabela
    for linha_paises in tabela_paises.findChildren(['tr']):
        #pego as celulas de cada linha, a primeira célula é o código do país. A quinta célula é a listagem de países que usam essa moeda
        celulas_paises = linha_paises.findChildren(['td'])
        #verifico se tem o tamanho correto e é um valor válido para salvar
        if(len(celulas_paises)>=4):
            #pego o código(Primeira célula)
            codigo_pais = celulas_paises[0].string
            #verifico todos os links na quinta célular para encontrar o nome de todos os países
            nomes_paises = []
            ahref_nomes_paises = celulas_paises[4].findAll(['a'])
            for nomep in ahref_nomes_paises:
                nomes_paises.append(nomep.string)
            #salvo o código como chave de um dicionário com seu valor sendo um array dos paises
            dict_paises[codigo_pais] = nomes_paises
    
    return dict_paises    
    
    
    '''
    #====Código utilizado para Web Scrapping em outra página========
    #Pegamos os nomes e códigos separadamente, mas ambos possuem a mesma quantidade no site
    #pega todos os links na tabela de paises, seus títulos são os nomes dos países
    nomes_paises=[]
    for nomes_paises_ahref in tabela_paises.findChildren(['a']):
        nomes_paises.append(nomes_paises_ahref.get('title'))
    
    #pega todas linhas da tabela, elas contêm o código
    codigos_paises=[]
    linhas_paises = tabela_paises.findChildren(['tr'])
    for codigo_pais_atual in codigos_e_paises:
        #pega as células da linha, o primeiro valor é a célula com o código
        celulas_paises = codigo_pais_atual.findChildren('td')
        codigo_pais=val_codigo_pais[0].string
        #salva no vetor de código
        if(codigo_pais!=None):
            codigos_paises.append(codigo_pais)
            
    #retorna um dicionario com os códigos como chave e nomes dos países como valores
    return dict(zip(codigos_paises, nomes_paises))
    '''



def acha_infos_menor_dolar(df_moedas):    
    #pega a linha do dataframe de moedas que tenha o menor valor do dólar
    menor_moeda = df_moedas[df_moedas["Valor_dolar"]==df_moedas["Valor_dolar"].min()]
    
    #pega os valores que queremos, usa iloc para pegar o único valor e seu conteúdo
    simbolo_moeda = menor_moeda["Moeda"].iloc(0)[0]
    cotacao_moeda = menor_moeda["Valor_dolar"].iloc(0)[0]
    #Utiliza web scrapping para pegar listagem de nome do país em português
    dict_paises = gera_listagem_nomes_pais()
    #Uso o dicionario dos países para pegar a listagem de países dado o símbolo da moeda
    paises_moeda = dict_paises[simbolo_moeda]
    
    return simbolo_moeda, paises_moeda,cotacao_moeda
    
    
def retorna_resultado_menor_cotacao(simbolo_moeda,paises_moeda,cotacao_moeda):
    #printa as saidas
    print(simbolo_moeda, end = ',')
    #printa os paises fora do array
    for pais in paises_moeda:
        print(pais, end = ',')
    print(cotacao_moeda)


if __name__ == "__main__":
    df_moedas_cotacao = gera_dataframe_moedas_cotacao(1,1,1)
    df_moedas_cotacao = calcular_dolar_df(df_moedas_cotacao,MONTANTE)
    simbolo, paises, cotacao = acha_infos_menor_dolar(df_moedas_cotacao)
    retorna_resultado_menor_cotacao(simbolo,paises,cotacao)