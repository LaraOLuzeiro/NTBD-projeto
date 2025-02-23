import psycopg2
import csv

# Dados de conexão
host = "localhost"
database = "Conab_DW"
user = "postgres"
password = "y1u2g3o4"
port = "5432"  # Porta padrão do PostgreSQL

# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    print("Conexão bem-sucedida!")

    cursor = conn.cursor()

    # Ler arquivo CSV que contém os dados brutos e puxar os dados das
    # Dimensões para inserir na tabela de fato
    with open('produtos_final.csv', 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)

        next(leitor) # Pula a primeira linha (cabeçalho)

        # Iterar sobre as linhas do arquivo
        for linha in leitor:

            nome_produto = linha[0]
            nivel_comercializacao = linha[1]
            estado = linha[2]
            mes = linha[3]
            ano = linha[4]
            preco_medio = linha[5]
            cursor.execute("""
            INSERT INTO Fato_Cotacao (pk_produto, pk_tempo, pk_comercializacao, pk_local, preco)
            SELECT pk_produto, pk_tempo, %s, pk_local, %s
            FROM Dimensao_Produto dp
            JOIN Dimensao_Local dl ON (dl.estado = %s)
            JOIN Dimensao_Tempo dt ON (dt.mes = %s) AND (dt.ano = %s)
            WHERE dp.nome_produto = %s
        """, (nivel_comercializacao, preco_medio, estado, mes, ano, nome_produto))
            conn.commit()  # Salva as alterações

except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
finally:
    # Certifique-se de fechar a conexão
    cursor.close()
    conn.close()