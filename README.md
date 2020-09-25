# Desafio de Programacao-Cotacao de Moeda
 Desafio de Programação apresentado em processo seletivo com objetivo de obter a moeda com menor cotação de dólar.
 
# Solução do Problema
 O código apresentado utiliza o arquivo csv disponibilizado pelo Banco Central. O arquivo csv que é usado pode ser acessado pelo link https://www.bcb.gov.br/estabilidadefinanceira/cotacoestodas.
 Através desse arquivo, conseguimos pegar os valores de dólar de cada moeda.
 
 Para execução do código, basta executar o arquivo menor_cotacao_data_especifica.py com python3. Insira a data e um csv será pego, se possível, do site. Um dataframe vai ser gerado com as informações da moeda para o cálculo do dolar, e por fim, será encontrado o menor valor do dólar e retornado as informações desejadas.
 Para descobrir o nome do país, é feito um web scrapping na página de link https://pt.wikipedia.org/wiki/ISO_4217 da Wikipedia, retornando o código da Moeda e seu nome. Através dessa ligação é possível gerar os nomes dos países que usam cada moeda.

#Bibliotecas necessárias:
 - requests
 - pandas
 - BeautifulSoup
 
# Problema apresentado:

Você foi contratado como freelancer por uma empresa de análise de dados que precisa de uma solução para o seguinte problema:

Todos os dias a empresa precisa saber qual moeda possui a menor cotação frente ao dólar. Essa informação é importante para uma outra aplicação de ranking de moedas que eles irão desenvolver.

O gerente da empresa que te contratou te passou o link do banco central (https://www.bcb.gov.br/) como referência. Ele mesmo também não conhece o site do BC detalhadamente para indicar o lugar exato da fonte de dados, mas sabe que é possível baixar um arquivo com os dados desejados a partir do portal.

Neste momento, o que eles precisam é um programa que receba uma data no formato `YYYYMMDD` via terminal e exiba na saída uma linha com as seguintes informações separadas por vírgula:

    - o símbolo da moeda com menor cotação,
    - o nome do país de origem da moeda e
    - o valor da cotação desta moeda frente ao dólar na data especificada.
Caso não haja cotação no dia especificado o caracter `x` deve ser impresso na tela.


Escreva um programa que atenda aos requisitos acima.
