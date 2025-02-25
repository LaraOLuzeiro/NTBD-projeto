import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2

# Função para mapear o código da UF para a região
def atribui_regiao(cod):
    if cod.startswith('1'):
        return "Norte"
    elif cod.startswith('2'):
        return "Nordeste"
    elif cod.startswith('3'):
        return "Sudeste"
    elif cod.startswith('4'):
        return "Sul"
    elif cod.startswith('5'):
        return "Centro-Oeste"
    return "Desconhecido"  # Caso o código não se encaixe em nenhum critério

# Função para fazer o scraping dos dados do IBGE
def scraper_ibge():
    url = "https://www.ibge.gov.br/explica/codigos-dos-municipios.php"
    response = requests.get(url)
    response.raise_for_status()  
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("tbody", class_="codigos-list")
    
    estados = []
    
    if table:
        rows = table.find_all("tr", class_="uf data-line")
        for row in rows:
            cols = row.find_all("td")
            nome_estado = cols[0].text.strip()
            codigo = cols[1].text.strip().split("ver municípios")[0].strip()
            regiao = atribui_regiao(codigo)
            estados.append({
                "estado": nome_estado,
                "regiao": regiao,
                "pais": "Brasil"
            })

    # Criando um DataFrame com os dados extraídos
    df = pd.DataFrame(estados)
    return df

# Função para inserir os dados no banco de dados
def inserts(df, table_name):
    # Lista para armazenar os comandos INSERT
    inserts = []

    # Itera sobre as linhas do DataFrame
    for index, row in df.iterrows():
        # Cria a lista de valores a serem inseridos
        values = ', '.join([f"'{str(value)}'" for value in row])
        
        # Cria o comando INSERT INTO
        insert = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});"
        
        # Adiciona o comando à lista
        inserts.append(insert)
    
    return inserts

def inserir_bd(df, table_name):
    # Conexão com o banco de dados PostgreSQL
    connection_string = "postgresql://postgres:SUA_SENHA@localhost:5432/Conab_DW"
    
    # Conectando ao banco de dados
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Gerar os comandos INSERT  
    insert = inserts(df, table_name)

    # Executar cada comando INSERT
    for statement in insert:
        try:
            cursor.execute(statement)
            conn.commit()  # Confirma a transação
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            conn.rollback()  # Desfaz a transação em caso de erro

    # Fecha a conexão
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Scrape dos dados
    df = scraper_ibge()

    # Inserção no banco de dados
    inserir_bd(df, 'Dimensao_Local')
    
    print("Dados inseridos com sucesso!")
