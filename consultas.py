import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Conexão com o banco de dados
conn = psycopg2.connect(
	host = "localhost",
	database = "Conab_DW",
	user = "postgres",
	password = "y1u2g3o4",  # Senha do banco de dados
	port = "5432"  # Porta padrão do PostgreSQL
)

# RENAN
# Qual a média dos preços do ABACAXI HAVAÍ (kg) ao longo dos anos no estado do Paraná

query_renan = """
SELECT dt.ano, AVG(fc.preco) AS preco_medio
FROM Fato_Cotacao fc
JOIN Dimensao_Tempo dt ON fc.PK_tempo = dt.PK_tempo
JOIN Dimensao_Produto dp ON fc.PK_produto = dp.PK_produto
JOIN Dimensao_Local dl ON fc.PK_local = dl.PK_local
WHERE dp.nome_produto = 'ABACAXI HAVAÍ (kg)' AND dl.estado = 'Paraná'
GROUP BY dt.ano
ORDER BY dt.ano;
"""

# Executar a consulta e carregar os dados em um DataFrame
df_renan = pd.read_sql(query_renan, conn)

# Criação do gráfico
plt.figure(figsize=(20, 10))
plt.plot(df_renan["ano"], df_renan["preco_medio"], marker='o', linestyle='-', color='b')

# Configurações do gráfico
plt.xlabel("Ano")
plt.ylabel("Preço Médio (R$)")
plt.title("Evolução do Preço do Abacaxi Havaí (kg) no Paraná")
plt.grid(True)

# Exibir o gráfico
plt.show()


"""
--Daniella

-- Quantos porcento caiu o preço da CARNE BOVINA DIANTEIRO COM OSSO (15 kg) no Amazonas de fevereiro de 2023 para outubro de 2023?
SELECT distinct nome_produto, estado, ROUND(((SELECT preco FROM preco_fevereiro_e_outubro WHERE mes_por_extenso = 'Outubro') * 100 / (SELECT preco FROM preco_fevereiro_e_outubro WHERE mes_por_extenso = 'Fevereiro')) :: NUMERIC, 2) AS porcentagem
from preco_fevereiro_e_outubro

CREATE OR REPLACE VIEW preco_fevereiro_e_outubro(nome_produto, estado, mes_por_extenso, ano, preco) AS
	SELECT nome_produto, estado, mes_por_extenso, ano, preco
	FROM fato_cotacao NATURAL JOIN Dimensao_tempo NATURAL JOIN dimensao_local NATURAL JOIN dimensao_produto
	WHERE nome_produto = 'CARNE BOVINA DIANTEIRO COM OSSO (15 kg)' AND estado = 'Amazonas' AND ano = 2023 AND mes_por_extenso = 'Fevereiro' 
	UNION  
	SELECT nome_produto, estado, mes_por_extenso, ano, preco
	FROM fato_cotacao NATURAL JOIN Dimensao_tempo NATURAL JOIN dimensao_local NATURAL JOIN dimensao_produto
	WHERE nome_produto = 'CARNE BOVINA DIANTEIRO COM OSSO (15 kg)' AND estado = 'Amazonas' AND ano = 2023 AND mes_por_extenso = 'Outubro';

"""
conn.close()