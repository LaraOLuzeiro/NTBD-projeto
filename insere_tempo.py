import pandas as pd
import psycopg2
import locale

# Definir o locale para português
locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

def generate_insert_statements(table_name):

    # Lista para armazenar os comandos SQL
    insert_statements = []

    # Criar uma sequência de datas de janeiro de 2014 até janeiro de 2025
    datas = pd.date_range(start="2000-01", end="2025-02", freq="MS")  # 'MS' = Start of Month

    # Gerar os inserts
    for data in datas:
        mes_numero = data.month  
        mes_nome = data.strftime("%B").capitalize()   # Nome do mês 
        ano = data.year 
        trimestre = data.quarter 

        # Criar o comando SQL
        insert_statement = f"INSERT INTO {table_name} (mes, ano, trimestre, mes_por_extenso) VALUES ({mes_numero}, {ano}, {trimestre}, '{mes_nome}');"
        insert_statements.append(insert_statement)

    return insert_statements


def insert_data_into_db(table_name):
    # Conexão com o banco de dados PostgreSQL
    connection_string = "postgresql://postgres:y1u2g3o4@localhost:5432/Conab_DW"
    #connection_string = "postgresql://postgres:lara14ufscar@localhost:5432/Conab_DW"
    
    # Conectando ao banco de dados
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Gerar os comandos INSERT
    insert_statements = generate_insert_statements(table_name)

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


    # Inserção no banco de dados
    insert_data_into_db('Dimensao_Tempo')
    
    print("Dados inseridos com sucesso!")