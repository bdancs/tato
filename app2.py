import pandas as pd
import requests

input_file = 'dados_api_filtrados.xlsx'

# Pega o arquivo excel e deixa o orgao_cnpj como string caso tenha 0 a esquerda
df = pd.read_excel('dados_api_filtrados.xlsx', dtype={'orgao_cnpj': str})

all_items = []

# Contador de progresso
total_rows = len(df)
current_row = 0

# Iterar sobre cada linha do DataFrame
for index, row in df.iterrows():
    current_row += 1
    print(f'Processando {current_row}/{total_rows}...')

    # Extrair dados das colunas
    orgao_cnpj = row['orgao_cnpj']
    ano = row['ano']
    numero = row['numero_sequencial']
    title = row['title']            # Adicionar aqui colunas desejadas do primeiro arquivo
    description = row['description']  

    # Verificar se os valores necessários não são nulos
    if pd.isnull(orgao_cnpj) or pd.isnull(ano) or pd.isnull(numero):
        print(f'Linha {index}: Valores necessários estão faltando. Pulando esta linha.')
        continue  # Pula para a próxima iteração

    # Converte valores para string
    orgao_cnpj = str(orgao_cnpj).strip()
    ano = str(int(ano)).strip()
    numero = str(numero).strip()

    # Url da api
    api_url = f'https://pncp.gov.br/api/pncp/v1/orgaos/{orgao_cnpj}/compras/{ano}/{numero}/itens?pagina=1&tamanhoPagina=9000'

    try:
        # Fazer chamada da api
        response = requests.get(api_url)
        response.raise_for_status()  # Excessão de código

        # transforma a resposta para json
        data = response.json()

        if data:
            for item in data:
                # Adicionar informações de contexto, se necessário
                item['orgao_cnpj'] = orgao_cnpj
                item['ano'] = ano
                item['numero_sequencial'] = numero
                item['title'] = title                # Adicionar aqui colunas desejadas do primeiro arquivo
                item['description'] = description

            all_items.extend(data)
        else:
            print(f'Linha {index}: Nenhum item retornado pela API.')
    except requests.exceptions.HTTPError as http_err:
        print(f'Erro HTTP na linha {index}: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Erro ao acessar a API na linha {index}: {err}')
    except Exception as e:
        print(f'Erro inesperado na linha {index}: {e}')

# Verificar se itens foram coletados
if all_items:
    # Criar um DataFrame com todos os itens
    items_df = pd.DataFrame(all_items)

    #Colocar todas colunas desejadas
    colunas_desejadas = [
        'title',
        'description',
        'numeroItem',
        'descricao',
        'materialOuServico',
        'materialOuServicoNome',
        'valorUnitarioEstimado',
        'valorTotal',
        'quantidade',
        'unidadeMedida',
        'orcamentoSigiloso',
        'itemCategoriaId'
    ]

    # Verificar se todas as colunas existem no DataFrame
    df_filtrado = items_df[items_df['materialOuServico'] == 'M']
    df_filtrado_orcamento = df_filtrado[df_filtrado['orcamentoSigiloso'] == False]
    colunas_existentes = [col for col in colunas_desejadas if col in df_filtrado_orcamento.columns]

    df_filtrado_orcamento = df_filtrado_orcamento[colunas_existentes]

    print(df_filtrado_orcamento.head(2))
    # Salvar em um arquivo Excel
    df_filtrado_orcamento.to_excel('itens_coletados.xlsx', index=False)
    print('Todos os itens foram salvos em "itens_coletados.xlsx"')
else:
    print('Nenhum item foi coletado da API.')
