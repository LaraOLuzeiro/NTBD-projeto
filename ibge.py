# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # Inicializar WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Acessa a página do IBGE
# driver.get('https://www.ibge.gov.br/explica/codigos-dos-municipios.php')

# # Aguarda o carregamento da página
# time.sleep(5)  # Ajuste o tempo conforme necessário

# # Lista para armazenar os nomes das cidades com a UF
# cidades_com_uf = []

# # Encontra todas as tabelas de municípios
# tabelas = driver.find_elements(By.CSS_SELECTOR, "tbody.codigos-list")

# # Itera sobre as tabelas e coleta os nomes das cidades com a UF
# for tabela in tabelas:
#     # Encontra o <thead> anterior à tabela atual para obter a UF
#     thead = tabela.find_element(By.XPATH, "./preceding-sibling::thead[1]")
#     uf = thead.get_attribute("id")  # O ID do <thead> é a sigla da UF
    
#     # Itera sobre as linhas da tabela para coletar os nomes das cidades
#     linhas = tabela.find_elements(By.CSS_SELECTOR, "tr.municipio.data-line")
#     for linha in linhas:
#         cidade = linha.find_element(By.CSS_SELECTOR, "td > a").text
#         cidades_com_uf.append(f"{uf}_{cidade}")

# # Fecha o navegador
# driver.quit()

# # Exibe os nomes das cidades com a UF
# for cidade_uf in cidades_com_uf:
#     print(cidade_uf)

# # Salva os nomes das cidades com a UF em um arquivo (opcional)
# with open("cidades_ibge_com_uf.txt", "w") as arquivo:
#     for cidade_uf in cidades_com_uf:
#         arquivo.write(cidade_uf + "\n")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Função para mapear o código da UF para a região
def get_region_by_code(uf_code):
    if uf_code.startswith('1'):
        return "Norte"
    elif uf_code.startswith('2'):
        return "Nordeste"
    elif uf_code.startswith('3'):
        return "Sudeste"
    elif uf_code.startswith('4'):
        return "Sul"
    elif uf_code.startswith('5'):
        return "Centro-Oeste"
    return "Desconhecido"  # Caso o código não se encaixe em nenhum critério

# Função para fazer o scraping dos dados do IBGE
def scrape_ibge_states():
    url = "https://www.ibge.gov.br/explica/codigos-dos-municipios.php"
    response = requests.get(url)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("tbody", class_="codigos-list")
    
    states_data = []
    
    if table:
        rows = table.find_all("tr", class_="uf data-line")
        for row in rows:
            cols = row.find_all("td")
            state_name = cols[0].text.strip()
            uf_code = cols[1].text.strip().split("ver municípios")[0].strip()
            uf_abbr = cols[0].find("a")["href"].replace("#", "")
            region = get_region_by_code(uf_code)
            states_data.append({
                "estado": state_name,
                "regiao": region,
                "pais": "Brasil"
            })

    # Criando um DataFrame com os dados extraídos
    df = pd.DataFrame(states_data)
    return df

# Função para inserir os dados no banco de dados
def insert_data_into_db(df):
    # Conexão com o banco de dados PostgreSQL
    connection_string = "postgresql://username:password@localhost:5432/database_name"  # Substitua pelos seus dados de conexão
    engine = create_engine(connection_string)

    # Inserindo os dados no banco de dados
    df.to_sql('Dimensao_Local', engine, if_exists='append', index=False)

if __name__ == "__main__":
    # Scrape dos dados
    df = scrape_ibge_states()
    
    # Inserção no banco de dados
    insert_data_into_db(df)
    
    print("Dados inseridos com sucesso!")
