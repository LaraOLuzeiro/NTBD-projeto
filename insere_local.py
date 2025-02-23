import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2

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
    response.raise_for_status()  
    
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
def generate_insert_statements(df, table_name):
    # Lista para armazenar os comandos INSERT
    insert_statements = []

    # Itera sobre as linhas do DataFrame
    for index, row in df.iterrows():
        # Cria a lista de valores a serem inseridos
        values = ', '.join([f"'{str(value)}'" for value in row])
        
        # Cria o comando INSERT INTO
        insert_statement = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});"
        
        # Adiciona o comando à lista
        insert_statements.append(insert_statement)
    
    return insert_statements

def insert_data_into_db(df, table_name):
    # Conexão com o banco de dados PostgreSQL
    connection_string = "postgresql://postgres:y1u2g3o4@localhost:5432/Conab_DW"
    
    # Conectando ao banco de dados
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Gerar os comandos INSERT  
    insert_statements = generate_insert_statements(df, table_name)

    # Executar cada comando INSERT
    for statement in insert_statements:
        try:
            cursor.execute(statement)
            conn.commit()  # Confirma a transação
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            conn.rollback()  # Desfaz a transação em caso de erro

    # Fechar a conexão
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Scrape dos dados
    df = scrape_ibge_states()

    print(df.head())  # Exibir as primeiras linhas do DataFrame
    
    # Inserção no banco de dados
    insert_data_into_db(df, 'Dimensao_Local')
    
    print("Dados inseridos com sucesso!")
