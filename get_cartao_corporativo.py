# Documentação da API oferecida pelo portal Transparência Brasil: https://api.portaldatransparencia.gov.br/swagger-ui.html

import requests
import key
import pandas as pd
import json
from datetime import datetime, timedelta

link = "http://api.portaldatransparencia.gov.br/api-de-dados/cartoes"

s = requests.Session()
s.headers.update({'chave-api-dados': key.value})


def get_date_today():
    today = datetime.now()
    return today.strftime("%d/%m/%Y")


# Se você quiser usar uma função que facilite consulta em um intervalo de dias;
# ex: últimos 30, 60, 90 dias
def get_date(days_to_subtract):
    last_day = datetime.now()
    return last_day - timedelta(days=days_to_subtract)


def get_dados(paginas):
    data = []
    today = get_date_today()

    for i in range(1, paginas):
        payload = {'codigoOrgao': 20101, 'dataTransacaoInicio': '01/01/2019',
                   'dataTransacaoFim': today, 'pagina': i}
        response = s.get(link, params=payload)
        pgdata = json.loads(response.content)
        data.append(pgdata[0])

    return data


def save_dataframe(lista_dicionarios):
    df = pd.json_normalize(lista_dicionarios)
    # print(df.columns)
    labels = [
        'id', 'mes_extrato', 'data_transacao', 'valor', 'id_tipo_cartao',
        'cod_tipo_cartao', 'desc_tipo_cartao', 'id_fornecedor',
        'cpf_fornecedor', 'cnpj_fornecedor', 'insc_social_fornecedor',
        'nome_fornecedor', 'razao_social_fornecedor', 'nome_fantasia_fornecedor',
        'tipo_fornecedor', 'cod_ug', 'nome_ug', 'desc_ug',
        'cod_orgao_vinculado', 'cnpj_ovinc', 'sigla_ovinc', 'nome_ovinc',
        'cod_orgao_maximo', 'sigla_omax', 'nome_omax', 'cpf_portador',
        'nis_portador', 'nome_portador'
    ]
    df.columns = labels
    df.to_csv('dados/cartao_corporativo', sep=';',
              encoding='utf-8', index=False)
    df.head(10)


# Infelizmente, a única forma de descobrir a quantidade de páginas é consultando a API (swagger ou postman/insomnia)
card_expenses = get_dados(196)
save_dataframe(card_expenses)
