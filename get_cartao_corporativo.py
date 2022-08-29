# Documentação Requests: https://requests.readthedocs.io/en/latest/user/quickstart/
# Swagger Transparência Brasil: https://api.portaldatransparencia.gov.br/swagger-ui.html

import requests
import json
import chave
from datetime import datetime, timedelta
import pandas as pd

def dia_atual():
    hoje = datetime.now()
    return hoje.strftime("%d/%m/%Y")


# Se você quiser usar uma funcao que facilite a consulta em um intervalo de dias:
def gera_data(variacao_dias):
    hoje = datetime.now()
    data_inicial = hoje-timedelta(days=variacao_dias)
    return data_inicial.strftime("%d/%m/%Y")


def consulta_cartoes(sessao, api, paginas, data_inicial, data_final):
    lista_resultados = []
    parametros = {
        'codigoOrgao': '20101',
        'dataTransacaoInicio': data_inicial,
        'dataTransacaoFim': data_final,
        'pagina': 1
    }
    for pg in range(1, paginas+1):
        parametros['pagina'] = pg
        resposta = sessao.get(api, params=parametros)
        if resposta.status_code == 200:
            dados_pg = json.loads(resposta.content)
            for dado in dados_pg:
                lista_resultados.append(dado)
        else:
            print(f"Erro na requisição, pg {pg}")
    print(f"Total de resultados: {len(lista_resultados)}")
    return lista_resultados


def salvar_dataframe(lista_dicionarios):
    df = pd.json_normalize(lista_dicionarios)
    # print(df.columns)
    labels = [
        'id', 'mes_extrato', 'data_transacao', 'valor', 'id_tipo_cartao',
        'cod_tipo_cartao', 'desc_tipo_cartao', 'id_fornecedor',
        'cpf_fornecedor', 'cnpj_fornecedor', 'insc_social_fornecedor',
        'nome_fornecedor', 'razao_social_fornecedor', 'nome_fantasia_fornecedor',
        'tipo_fornecedor', 'cod_unidade_gestora', 'nome_ug', 'desc_ug',
        'cod_orgao_vinculado', 'cnpj_ovinc', 'sigla_ovinc', 'nome_ovinc',
        'cod_orgao_maximo', 'sigla_omax', 'nome_omax', 'cpf_portador',
        'nis_portador', 'nome_portador'
    ]
    df.columns = labels
    df.to_csv('dados/cartao_corporativo_PR_2019_2022', sep=';',
              encoding='utf-8', index=False)
    
    
def requisicao_api_transparencia():
    api = "http://api.portaldatransparencia.gov.br/api-de-dados/cartoes"
    sessao = requests.Session()
    sessao.headers.update({'chave-api-dados': chave.valor})
    hoje = dia_atual()
    dados = consulta_cartoes(sessao, api, 202, "01/01/2019", hoje)
    salvar_dataframe(dados)

# Infelizmente, a única forma de descobrir a quantidade de páginas é consultando a API (usar "try" no swagger ou o postman/insomnia)
