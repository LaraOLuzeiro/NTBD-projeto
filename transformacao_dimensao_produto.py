import re

# Função para processar o arquivo SQL e garantir que cada produto tenha apenas uma categoria
def processar_arquivo_sql(caminho_entrada, caminho_saida):
    produtos = {}  # Dicionário para armazenar os produtos e suas categorias

    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_entrada:
        for linha in arquivo_entrada:
            if linha.startswith("INSERT INTO Dimensao_Produto"):
                # Remover vírgulas do nome do produto antes de processar
                linha = remove_commas_from_product_name(linha)

                # Extrair o nome do produto e a categoria
                partes = linha.split("VALUES")[1].strip().strip("();").split(", ")
                nome_produto = partes[0].strip("'")
                categoria = partes[1].strip("'")

                # Se o produto já existe no dicionário, mantemos a primeira categoria encontrada
                if nome_produto not in produtos:
                    produtos[nome_produto] = categoria

    # Escrever o arquivo final sem precisar do intermediário
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        for nome_produto, categoria in produtos.items():
            linha_sql = f"INSERT INTO Dimensao_Produto (nome_produto, cultura_especie) VALUES ('{nome_produto}', '{categoria}');\n"
            arquivo_saida.write(linha_sql)

# Função para remover vírgulas do nome do produto
def remove_commas_from_product_name(line):
    match = re.match(r"(INSERT INTO Dimensao_Produto \(nome_produto, cultura_especie\) VALUES \()'(.*?)'(, '.*?'\);)", line)
    if match:
        prefix = match.group(1)
        product_name = match.group(2).replace(",", "")  # Remove vírgulas do nome do produto
        suffix = match.group(3)
        return f"{prefix}'{product_name}'{suffix}\n"
    return line

# Caminho do arquivo SQL de entrada e saída
input_file = 'insert_dimensao_produto_intermediario.sql'
output_file = 'insert_dimensao_produto_final.sql'

# Processar o arquivo diretamente e gerar o arquivo final
processar_arquivo_sql(input_file, output_file)

print(f"Arquivo processado e salvo em: {output_file}")
