import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa o WebDriver com o webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get('https://consultaprecosdemercado.conab.gov.br/#/home')
time.sleep(2)

# Seleciona preços mensais
botao_preco_mensal = driver.find_element(By.XPATH, "//button[.//i[contains(@class, 'fa-th-large')]]")
botao_preco_mensal.click()

# Selecionando períodos para consultar
periodos = [
    (0, 11, 11, 8),  # Jan/2014 - Dez/2017
    (0, 7, 11, 4),   # Jan/2018 - Dez/2021
    (0, 3, 0, 0)   # Jan/2022 - Jan/2025
]

# Lista para armazenar os comandos SQL
insert_statements = []

# Nome da tabela no banco de dados
table_name = "Dimensao_Produto"

with open("produtos3.csv", "w", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(["nome_produto", "nivel_comercializacao", "estado", "mes_ano", "preco_medio"])

    for periodo_mes_inicial, periodo_ano_inicial, periodo_mes_final, periodo_ano_final in periodos:

        # Selecionar o mês inicial 
        mes_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesInicial")))
        mes_inicial_dropdown.click()
        mes_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='mesInicial{periodo_mes_inicial}']")))  
        mes_inicial.click()

        # Selecionar o ano inicial 
        ano_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoInicial")))
        ano_inicial_dropdown.click()
        ano_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='anoInicial{periodo_ano_inicial}']")))  
        ano_inicial.click()

        # Selecionar o mês final 
        mes_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesFinal")))
        mes_final_dropdown.click()
        mes_final = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='mesFinal{periodo_mes_final}']")))  
        mes_final.click()

        # Selecionar o ano final 
        ano_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoFinal")))
        ano_final_dropdown.click()
        ano_final = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='anoFinal{periodo_ano_final}']")))  
        ano_final.click()

        # Selecionando botões Pesquisar e Consultar
        botao_pesquisar = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
        botao_pesquisar.click()
        time.sleep(2)
        botao_consultar = driver.find_element(By.XPATH, "//button[contains(text(), 'Consultar')]")
        botao_consultar.click()
        time.sleep(2)

        # Selecionando máximo de 100 resultados por página
        botoes_selecao = driver.find_elements(By.XPATH, "//button[@aria-label='Exibir lista']")
        botao_selecao = botoes_selecao[7]
        botao_selecao.click()
        botao_selecao = driver.find_element(By.CSS_SELECTOR, "label[for='per-page-selection-random5']")
        botao_selecao.click()

        while True:
            try:
                # Aguarda até que os resultados estejam na página
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'tr'))
                )

                time.sleep(2)
                
                resultados = driver.find_elements(By.TAG_NAME, 'tr')

                produto_atual = None
                nivel_atual = None
                estado_atual = None

                for resultado in resultados[1:101]:
                    colunas = [coluna.text.strip() for coluna in resultado.find_elements("tag name", "td")]

                    if colunas[0] == "" and colunas[1] == "" and colunas[2] == "" and colunas[3] == "" and colunas[4] =="":
                        continue  # Ignora linhas inesperadas

                    # Apenas mes_ano e preco_medio, mantém os valores anteriores
                    elif colunas[0] == "" and colunas[1] == "" and colunas[2] == "":
                        mes_ano = colunas[3]
                        preco_medio = colunas[4]
                        writer.writerow([produto_atual, nivel_atual, estado_atual, mes_ano, preco_medio])

                    # Apenas nivel, estado, mes_ano e preco_medio, mantém o valor do produto
                    elif colunas[0] == "":
                        nivel_atual = colunas[1]
                        estado_atual = colunas[2]
                        mes_ano = colunas[3]
                        preco_medio = colunas[4]
                        writer.writerow([produto_atual, nivel_atual, estado_atual, mes_ano, preco_medio])

                    # Nova linha completa, atualiza todos os campos
                    else:
                        produto_atual, nivel_atual, estado_atual, mes_ano, preco_medio = colunas
                        writer.writerow([produto_atual, nivel_atual, estado_atual, mes_ano, preco_medio])
                        with open("categoria.txt", "r", encoding="utf-8") as arquivo:
                            for numero_linha, linha in enumerate(arquivo, start=1):
                                if linha.strip() in produto_atual:
                                    # print(f"A string foi encontrada na linha {linha}")
                                    # Lendo o arquivo de categorias
                                    with open("categoria.txt", "r", encoding="utf-8") as file:
                                        categorias = [linha.strip().lower() for linha in file]  # Convertendo para minúsculas para evitar problemas de case

                                    # Verificando se a categoria está contida no nome_atual
                                    for categoria in categorias:
                                        if categoria in produto_atual.lower():  # Verifica se a categoria é um subconjunto do nome
                                            insert_statement = f"INSERT INTO {table_name} (nome_produto, cultura_especie) VALUES ('{produto_atual}', '{categoria}');"
                                            insert_statements.append(insert_statement)

                                    # Salvando os INSERTs em um arquivo .txt
                                    with open("inserts_dimensao_produto.sql", "w", encoding="utf-8") as file:
                                        for statement in insert_statements:
                                            file.write(statement + "\n")

                                    # print("Arquivo 'inserts.sql' gerado com sucesso!")
                                    break  # Para na primeira ocorrência
                                # else:
                                    # print("A string NÃO foi encontrada!")                        
                    
                # Verifica se o botão de próxima página está presente e habilitado
                try:
                    # Localiza o botão de próxima página pelo XPath
                    proxima_pagina = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Avançar página']"))
                    )
                    
                    # Verifica se o botão está desabilitado
                    if "disabled" in proxima_pagina.get_attribute("class"):
                        print("Fim das páginas.")
                        break

                    botao_proxima_pagina = driver.find_element(By.XPATH, "//button[@aria-label='Avançar página']")
                    botao_proxima_pagina.click()

                except Exception as e:
                    print("Botão de próxima página não encontrado:", e)
                    break

                # Aguarda um tempo adicional para garantir que a página seja carregada
                time.sleep(2)

                # Aguarda até que a nova página seja carregada
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'tr'))
                )

            except Exception as e:
                print(f"Erro: {e}")
                break

driver.quit()