# Imports
import numpy as np
import pandas as pd
import csv
import requests
import json

# Chamando a API pela url
# Precisamos chamar as APIs separadas ou as informações se misturam
url_pregao = "https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=9900&status=recebendo_proposta&q=comprasnet&tipos=1"
url_dispensa = "https://pncp.gov.br/api/search/?tipos_documento=edital"

# resto_pregao = 
# resto_dispensa = &ordenacao=-data&pagina=1&tam_pagina=9900&status=recebendo_proposta&tipos=2

# Faz a requisição para a API
response = requests.get(url_pregao)

# Verifica se a resposta foi bem-sucedida
if response.status_code == 200 :
    data = response.json()  # Converte a resposta para JSON
    
    # Extrai o conteúdo principal dos dados
    registros = data.get("resultados", [])  # Use a chave correspondente aos resultados na resposta da API
    
    # Define o nome do arquivo CSV de saída
    nome_arquivo_csv = "dados_api.csv"
    
    # Escreve os dados no CSV
    with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Escreve o cabeçalho
        if registros:
            headers = registros[0].keys()
            writer.writerow(headers)
        
            # Escreve cada registro no CSV
            for registro in registros:
                writer.writerow(registro.values())
        
        print(f"Arquivo CSV '{nome_arquivo_csv}' criado com sucesso!")
else:
    print(f"Erro ao chamar a API: {response.status_code}")