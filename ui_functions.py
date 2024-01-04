# pip install requests

# https://receitaws.com.br/api
# https://www.sintegraws.com.br/api/documentacao-api-receita-federal.php

import requests # Requisicao ao site da receita federal
import json     # pegar os dados em json da requisição


def consulta_cnpj(cnpj):
    #url = "http://www.receitaws.com.br/v1/cnpj/[cnpj]"

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}
    response = requests.request("GET", url, params = querystring)

    resp = json.loads(response.text)

    #print(response.text) # Mostra todas as informações 
    # Mostra uma informação específica :
    #print(resp['nome'])
    #print(resp['logradouro'])

    # Devolve uma lista com os campos desejados de resp
    return resp['nome'], resp['logradouro'], resp['numero'], resp['complemento'], resp['bairro'], resp['municipio'], resp['uf'], resp['cep'], resp['telefone'], resp['email']
    

# Se este arquivo que estiver sendo executado diretamente, 
#   rode o bloco de código dentro do "if" abaixo
#      
# https://www.youtube.com/watch?v=150-dpYG1pg

if(__name__ == "__main__"):
    # Esperar 20 segundos entre cada chamada a API. 
    # Ela tem um limite de resposta em modo gratuito 
    print(consulta_cnpj("33291488000102"))
    #print(consulta_cnpj("02683417000121"))
    #consulta_cnpj("02683417000121")
