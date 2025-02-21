import psycopg2

# Dados de conexão
host = "localhost"
database = "Conab_DW"
user = "postgres"
password = "lara14ufscar"
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
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

