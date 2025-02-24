"""ESTE ARQUIVO FOI CRIADO PARA REMOVER AS ASPAS DUPLAS DOS PRODUTOS, JÁ QUE ESSE DETALHE NÃO FOI TRATADO NO MOMENTO
DA CAPTURA DOS DADOS NA WEB. ALÉM DISSO, REMOVE TUPLAS DUPLICADAS."""

import csv
import pandas as pd

# Somente o campo nome_produto possui aspas duplas, então removemos elas e as vírgulas dentro dessas aspas.
# Por exemplo, "Produto, teste" vira Produto teste.
def remover_aspas_produtos(arquivo_entrada, arquivo_saida):
    count = 0
    with open(arquivo_entrada, 'r', newline='', encoding='utf-8') as arquivo_produtos:
        reader = csv.reader(arquivo_produtos)
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo_saida:
            writer = csv.writer(arquivo_saida)
            for linha in reader:
                nome_produto_corrigido = linha[0]       
                # As aspas duplas já são automaticamente removidas pelo Python CSV, então só precisamos remover as vírgulas.
                linha[0] = nome_produto_corrigido.replace(',', '')
                writer.writerow(linha)
                count += 1
                print(f'Corrigidos {count}: {linha}')

if __name__ == '__main__':
    remover_aspas_produtos('produtos_intermediario.csv', 'produtos_final.csv')

    # Removendo linhas duplicadas
    df = pd.read_csv('produtos_final.csv')
    df_limpo = df.drop_duplicates(subset=["nome_produto", "nivel_comercializacao", "estado", "mes", "ano"], keep="first")
    df_limpo.to_csv('produtos_final.csv', index=False)