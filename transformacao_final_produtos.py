"""ESTE ARQUIVO FOI CRIADO PARA REMOVER AS ASPAS DUPLAS DOS PRODUTOS, JÁ QUE ESSE DETALHE NÃO FOI TRATADO NO MOMENTO
DA CAPTURA DOS DADOS NA WEB. ALÉM DISSO, COMO JÁ TEMOS 165MIL TUPLAS, NÃO SERIA INTERESSANTE RODAR O WEB SCRAPING DO ZERO."""

import csv

# Somente o campo nome_produto possui aspas duplas, então removemos elas e as vírgulas dentro dessas aspas.
# Por exemplo, "Produto, teste" vira Produto teste.
def remover_aspas_produtos(nome_arquivo):
    nome_corrigido = None
    count = 0
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_produtos:
        reader = csv.reader(arquivo_produtos)
        with open('produtos_final.csv', 'w', newline='', encoding='utf-8') as arquivo_final:
            writer = csv.writer(arquivo_final)
            for linha in reader:
                nome_produto = linha[0]
                # Remove aspas duplas do nome
                if nome_produto.startswith('"') and nome_produto.endswith('"'):
                    nome_corrigido = nome_produto[1:-1]
                    # Remove vírgulas dentro do nome
                    nome_corrigido = nome_corrigido.replace(',', '')
                    writer.writerow([nome_corrigido, linha[1], linha[2], linha[3], linha[4], linha[5]])
                    count += 1
                    print(f"Corrigidos: {count} Produto {nome_corrigido}, {linha[1]}, {linha[2]}, {linha[3]}, {linha[4]}, {linha[5]}")
                else:
                    writer.writerow([nome_produto, linha[1], linha[2], linha[3], linha[4], linha[5]])
                    count += 1
                    print(f"Corrigidos: {count} Produto {nome_corrigido}, {linha[1]}, {linha[2]}, {linha[3]}, {linha[4]}, {linha[5]}")

if __name__ == '__main__':
    remover_aspas_produtos('produtos_intermediario.csv')