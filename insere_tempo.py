import pandas as pd
import psycopg2
import locale

# Definir o locale para português
locale.setlocale(locale.LC_ALL, "pt_br")

def insert_tempo(table_name):

    # Lista para armazenar os comandos SQL
    inserts = []

    # Criar uma sequência de datas de janeiro de 2000 até fevereiro de 2025
    datas = pd.date_range(start="2000-01", end="2025-02", freq="MS")  # 'MS' = Start of Month

    # Gerar os inserts
    for data in datas:
        mes_numero = data.month  
        mes_nome = data.strftime("%B").capitalize()   # Nome do mês 
        ano = data.year 
        trimestre = data.quarter 

        # Criar o comando SQL
        insert = f"INSERT INTO {table_name} (mes, ano, trimestre, mes_por_extenso) VALUES ({mes_numero}, {ano}, {trimestre}, '{mes_nome}');"
        inserts.append(insert)

    return inserts


#Função que insere os scripts de INSERT no banco de dados
def inserir_bd(table_name):
    # Conexão com o banco de dados PostgreSQL
    connection_string = "postgresql://postgres:SUA_SENHA@localhost:5432/Conab_DW"
    
    # Conectando ao banco de dados
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Gerar os comandos INSERT  
    inserts = insert_tempo(table_name)

    # Executar cada comando INSERT
    for i in inserts:
        try:
            cursor.execute(i)
            conn.commit()  # Confirma a transação
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            conn.rollback()  # Desfaz a transação em caso de erro

    # Fecha a conexão
    cursor.close()
    conn.close()

if __name__ == "__main__":

    # Inserção no banco de dados
    insere_bd('Dimensao_Tempo')
    
    print("Dados inseridos com sucesso!")