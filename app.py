import requests
import pandas as pd

# URLs das APIs
url1 = 'https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=20&status=recebendo_proposta&q=comprasnet&tipos=1&modalidades=7%7C6%7C8'
url2 = 'https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=20&status=recebendo_proposta&tipos=2&modalidades=7%7C6%7C8'

# Pega a api
def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        print(f'Erro ao acessar {url}: {response.status_code}')
        return []

# Pega os dados para cada api
data1 = get_data(url1)
data2 = get_data(url2)

# Junta as duas
all_data = data1 + data2

# Verificar se há dados
if all_data:
    # Converter para DataFrame
    df = pd.DataFrame(all_data)

    # Filtra só em unidade com 6 digitos
    df_filtrado = df[df['unidade_codigo'].str.len() == 6]

    # Verifica se ta vazio
    if not df_filtrado.empty:
        #Cria excel
        df_filtrado.to_excel('dados_api_filtrados.xlsx', index=False)
        print('Dados filtrados salvos em "dados_api_filtrados.xlsx"')
    else:
        print('Nenhuma linha com "unidade_codigo" de 6 dígitos foi encontrada.')
else:
    print('Nenhum dado foi obtido das APIs.')
