import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Conexão com o banco de dados
conn = psycopg2.connect(
	host = "localhost",
	database = "Conab_DW",
	user = "postgres",
	password = "y1u2g3o4",  # Senha do banco de dados
	port = "5432"  # Porta padrão do PostgreSQL
)

#Daniella

#Selecione o maior e o menor preco da BANANA PRATA (kg) em cada estado da regiao Nordeste durante o ano de 2017 com o nivel de comercialização ATACADO

query_daniella = """
SELECT estado, MAX(preco) AS maior_preco, MIN(preco) AS menor_preco
FROM fato_cotacao NATURAL JOIN Dimensao_tempo NATURAL JOIN dimensao_local NATURAL JOIN dimensao_produto
WHERE nome_produto = 'BANANA PRATA (kg)' AND regiao = 'Nordeste' AND ano = 2017 AND pk_comercializacao = 'ATACADO'
GROUP BY PK_produto, PK_local, estado;
"""

# Executar a consulta e carregar os dados em um DataFrame
df_daniella = pd.read_sql(query_daniella, conn)

# Criar uma posição para cada estado no eixo X
estados = df_daniella["estado"]
x = np.arange(len(estados))

# Largura das barras
largura = 0.4  

# Criar o gráfico de barras agrupadas
plt.figure(figsize=(12, 6))
plt.bar(x - largura/2, df_daniella["maior_preco"], largura, label="Maior Preço", color="royalblue")
plt.bar(x + largura/2, df_daniella["menor_preco"], largura, label="Menor Preço", color="lightcoral")

# Configurações do gráfico
plt.xlabel("Estado")
plt.ylabel("Preço (R$)")
plt.title("Maior e Menor Preço da Banana Prata (kg) no Nordeste em 2017")
plt.xticks(ticks=x, labels=estados, rotation=45)  # Ajustar rótulos dos estados
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Exibir o gráfico
plt.show()

# RENAN
# Qual a média dos preços do ABACAXI HAVAÍ (kg) ao longo dos anos no estado do Paraná, com nível de comercialização sendo PRODUTOR?

query_renan = """
SELECT dt.ano, AVG(fc.preco) AS preco_medio
FROM Fato_Cotacao fc
JOIN Dimensao_Tempo dt ON fc.PK_tempo = dt.PK_tempo
JOIN Dimensao_Produto dp ON fc.PK_produto = dp.PK_produto
JOIN Dimensao_Local dl ON fc.PK_local = dl.PK_local
WHERE dp.nome_produto = 'ABACAXI HAVAÍ (kg)' AND dl.estado = 'Paraná'
AND PK_comercializacao = 'PRODUTOR'
GROUP BY dt.ano
ORDER BY dt.ano;
"""

# Executar a consulta e carregar os dados em um DataFrame
df_renan = pd.read_sql(query_renan, conn)

# Criação do gráfico
plt.figure(figsize=(10, 5))
plt.plot(df_renan["ano"], df_renan["preco_medio"], marker='o', linestyle='-', color='b')

# Configurações do gráfico
plt.xlabel("Ano")
plt.ylabel("Preço Médio (R$)")
plt.title("Evolução do Preço do Abacaxi Havaí (kg) no Paraná")
plt.grid(True)

# Exibir o gráfico
plt.show()


# Lara
# Qual a média de preços de MANGA PALMER (kg) para cada mês do ano, considerando todos os anos disponíveis? O resultado deve conter o número do mês, o nome do mês e a média de preços naquele mês.

query_lara = """
SELECT mes, mes_por_extenso, AVG(preco) AS media_preco
FROM fato_cotacao NATURAL JOIN dimensao_tempo NATURAL JOIN dimensao_produto
WHERE nome_produto = 'MANGA PALMER (kg)'
GROUP BY mes, mes_por_extenso
ORDER BY mes;
"""

# Executar a consulta e carregar os dados em um DataFrame
df_lara = pd.read_sql(query_lara, conn)

# Cores
meses_especiais = ['Novembro', 'Dezembro', 'Janeiro']
cores = ["#33FFF3" if mes in meses_especiais else "#FF5733" for mes in df_lara["mes_por_extenso"]]

# Criar o gráfico de barras agrupadas
plt.figure(figsize=(12, 6))
plt.bar(df_lara["mes_por_extenso"], df_lara["media_preco"], color=cores)

# Configurações do gráfico
plt.xlabel("Mês")
plt.ylabel("Preço Médio (R$)")
plt.title("Média de preços da Manga Palmer (kg) por mês")

# Exibir o gráfico
plt.show()

conn.close()