import time 
import csv
import os 
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Função para carregar uma página com tratamento de exceções (caso internet caia por exemplo)
def carregar_pagina(url, delay=10):
    while True:
        try:
            driver.get(url)
            return
        except Exception as e:
            print(f"Erro ao carregar a página {url}: {e}. Tentando novamente em {delay} segundos...")
            time.sleep(delay)

# Função para clicar em um elemento com tratamento de exceções (caso internet caia por exemplo)
def clicar_elemento(by, localizador_elemento, delay=10, descricao=""):
    while True:
        try:
            element = wait.until(EC.element_to_be_clickable((by, localizador_elemento)))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            return
        except Exception as e:
            print(f"Erro ao clicar em {descricao}: {e}. Tentando novamente em {delay} segundos...")
            time.sleep(delay)

# Função para encontrar elementos com tratamento de exceções (caso internet caia por exemplo)
def encontrar_elemento(by, locator, delay=10, description=""):
    while True:
        try:
            elements = driver.find_elements(by, locator)
            if elements:
                return elements
            else:
                raise Exception("Nenhum elemento encontrado.")
        except Exception as e:
            print(f"Erro ao localizar elementos {description}: {e}. Tentando novamente em {delay} segundos...")
            time.sleep(delay)

# Inicializa o WebDriver com o webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

carregar_pagina('https://consultaprecosdemercado.conab.gov.br/#/home')

# Seleciona preços mensais
clicar_elemento(By.XPATH, "//button[.//i[contains(@class, 'fa-th-large')]]", descricao="botão de preços mensais")

# Lista para armazenar os comandos SQL
insert_statements = []

# Nome da tabela no banco de dados
table_name = "Dimensao_Produto"

# Conjunto auxiliar para verificar e evitar inserções duplicadas no arquivo de insert de produtos
produtos_inseridos = set() 

# Contador para ver o progresso da coleta dos produtos
count_produtos = 0 

# Retirada de dados do Conab fazendo alguns procedimentos de limpeza e transformação. 
# Inserção em arquivos intermediários para posterior tratamento final
with open("produtos_intermediario.csv", "a", newline="", encoding="utf-8") as arquivo:  
    writer = csv.writer(arquivo)
    writer.writerow(["nome_produto", "nivel_comercializacao", "estado", "mes", "ano", "preco_medio"]) 

    """NO TRECHO ABAIXO, A IDEIA ERA O SELENIUM AUTOMCATICAMENTE SELECIONAR OS MESES E ANOS. NO ENTANTO, APÓS A PRIMEIRA ITERAÇÃO NÃO CONSEGUIMOS
    FAZER RODAR DE FORMA CORRETA, E NÃO HOUVE TEMPO SUFICIENTE PARA MUDANÇA. ENTÃO, NO MOMENTO DE RODAR O PROGRAMA, O USUÁRIO DEVE SELECIONAR OS 
    MESES E ANOS MANUALMENTE ATRAVÉS DO ÍNDICE DA VARIÁVEL "periodo".    """

    periodos = [
    (0, 11, 11, 8),  # Jan/2014 - Dez/2017 
    (0, 7, 11, 4),   # Jan/2018 - Dez/2021 
    (0, 3, 0, 0)     # Jan/2022 - Jan/2025
    ]

    # Ajustar para o período desejado 0 = Jan/2014 - Dez/2017, 1 = Jan/2018 - Dez/2021, 2 = Jan/2022 - Jan/2025
    periodo_mes_inicial, periodo_ano_inicial, periodo_mes_final, periodo_ano_final = periodos[0] 

    # Selecionar o mês inicial 
    clicar_elemento(By.ID, "mesInicial", descricao="dropdown de mês inicial")
    clicar_elemento(By.XPATH, f"//label[@for='mesInicial{periodo_mes_inicial}']", descricao="mês inicial")

    # Selecionar o ano inicial 
    clicar_elemento(By.ID, "anoInicial", descricao="dropdown de ano inicial")  
    clicar_elemento(By.XPATH, f"//label[@for='anoInicial{periodo_ano_inicial}']", descricao="ano inicial")  

    # Selecionar o mês final 
    clicar_elemento(By.ID, "mesFinal", descricao="dropdown de mês final") 
    clicar_elemento(By.XPATH, f"//label[@for='mesFinal{periodo_mes_final}']", descricao="mês final")  

    # Selecionar o ano final 
    clicar_elemento(By.ID, "anoFinal", descricao="dropdown de ano final") 
    clicar_elemento(By.XPATH, f"//label[@for='anoFinal{periodo_ano_final}']", descricao="ano final")  

    # Selecionando botões Pesquisar e Consultar
    clicar_elemento(By.XPATH, "//button[contains(text(), 'Pesquisar')]", descricao="botão Pesquisar")
    time.sleep(2)
    clicar_elemento(By.XPATH, "//button[contains(text(), 'Consultar')]", descricao="botão Consultar")  
    time.sleep(2)

    # Selecionando máximo de 100 resultados por página
    while True: 
        try:
            botoes_selecao = encontrar_elemento(By.XPATH, "//button[@aria-label='Exibir lista']", description="botões Exibir lista")
            if len(botoes_selecao) < 8:
                raise Exception("Quantidade insuficiente de botões de exibir lista.")
            botoes_selecao[7].click()
            break
        except Exception as e:
            print(f"Erro ao selecionar botão de exibir lista: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
            
    while True: 
        try:
            botao_selecao = driver.find_element(By.CSS_SELECTOR, "label[for='per-page-selection-random5']")
            botao_selecao.click()
            break
        except Exception as e:
            print(f"Erro ao selecionar botão de 100 resultados por página: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)

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
            mes_ano = None
            mes = None
            ano = None
            preco_medio = None

            # Dicionário de siglas de UFs para passar UF para o nome completo
            uf_map = {
                'AC': 'Acre',
                'AL': 'Alagoas',
                'AP': 'Amapá',
                'AM': 'Amazonas',
                'BA': 'Bahia',
                'CE': 'Ceará',
                'DF': 'Distrito Federal',
                'ES': 'Espírito Santo',
                'GO': 'Goiás',
                'MA': 'Maranhão',
                'MT': 'Mato Grosso',
                'MS': 'Mato Grosso do Sul',
                'MG': 'Minas Gerais',
                'PA': 'Pará',
                'PB': 'Paraíba',
                'PR': 'Paraná',
                'PE': 'Pernambuco',
                'PI': 'Piauí',
                'RJ': 'Rio de Janeiro',
                'RN': 'Rio Grande do Norte',
                'RS': 'Rio Grande do Sul',
                'RO': 'Rondônia',
                'RR': 'Roraima',
                'SC': 'Santa Catarina',
                'SP': 'São Paulo',
                'SE': 'Sergipe',
                'TO': 'Tocantins'
            }

            for resultado in resultados[1:101]:
                colunas = [coluna.text.strip() for coluna in resultado.find_elements("tag name", "td")]

                if colunas[0] == "" and colunas[1] == "" and colunas[2] == "" and colunas[3] == "" and colunas[4] =="":
                    continue  # Ignora linhas inesperadas

                # Lógica somente para não inserir o produto 10-30-15 (50 kg)
                elif colunas[0] == '10-30-15 (50 kg)' or produto_atual == '10-30-15 (50 kg)':
                    if colunas[0] == "":
                        produto_atual = None
                        continue
                    produto_atual = '10-30-15 (50 kg)'
                    continue

                # Apenas mes_ano e preco_medio, mantém os valores anteriores
                elif colunas[0] == "" and colunas[1] == "" and colunas[2] == "":
                    mes_ano = colunas[3]
                    mes, ano = mes_ano.split('/')  # Divide a string em duas partes para facilitar inserção na tabela de fatos posteriormente
                    mes = int(mes) # Serve para retirar o zero à esquerda
                    preco_medio = colunas[4]
                    preco_medio = preco_medio.replace(',', '.')  # Substitui a vírgula por ponto para evitar problemas de compatibilidade com o PostgreSQL
                    writer.writerow([produto_atual, nivel_atual, estado_atual, mes, ano, preco_medio])

                    count_produtos += 1
                    print(f'Produtos Inseridos: {count_produtos}')

                # Apenas nivel, estado, mes_ano e preco_medio, mantém o valor do produto
                elif colunas[0] == "":
                    nivel_atual = colunas[1]
                    estado_atual = colunas[2]
                    estado_atual = uf_map.get(estado_atual) # Converte a sigla do estado para o nome completo
                    mes_ano = colunas[3]
                    mes, ano = mes_ano.split('/')  # Divide a string em duas partes para facilitar inserção na tabela de fatos posteriormente
                    mes = int(mes) # Serve para retirar o zero à esquerda
                    preco_medio = colunas[4]
                    preco_medio = preco_medio.replace(',', '.')  # Substitui a vírgula por ponto para evitar problemas de compatibilidade com o PostgreSQL
                    writer.writerow([produto_atual, nivel_atual, estado_atual, mes, ano, preco_medio])

                    count_produtos += 1
                    print(f'Produtos Inseridos: {count_produtos}')

                # Nova linha completa, atualiza todos os campos
                else:
                    produto_atual, nivel_atual, estado_atual, mes_ano, preco_medio = colunas
                    preco_medio = preco_medio.replace(',', '.')  # Substitui a vírgula por ponto para evitar problemas de compatibilidade com o PostgreSQL
                    mes, ano = mes_ano.split('/')  # Divide a string em duas partes para facilitar inserção na tabela de fatos posteriormente
                    mes = int(mes) # Serve para retirar o zero à esquerda                       
                    estado_atual = uf_map.get(estado_atual) # Converte a sigla do estado para o nome completo
                    writer.writerow([produto_atual, nivel_atual, estado_atual, mes, ano, preco_medio])

                    count_produtos += 1
                    print(f'Produtos Inseridos: {count_produtos}')

                    # Pega todas as categorias existentes no arquivo 'categoria.txt'
                    with open("categoria.txt", "r", encoding="utf-8") as arquivo:
                        for numero_linha, linha in enumerate(arquivo, start=1):
                            if linha.strip() in produto_atual:
                                # Lendo o arquivo de categorias
                                with open("categoria.txt", "r", encoding="utf-8") as file:
                                    categorias = [linha.strip().lower() for linha in file]  # Convertendo para minúsculas para evitar problemas de case

                                # Aproveitando o Web Scrapper para já criar o script de INSERTs para a dimensão de produtos
                                """COMO É NECESSÁRIO EXECUTAR TRÊS VEZES O PROGRAMA COM OS DETERMINADOS PERIODOS DE TEMPO, ENTÃO É PRECISO PEGAR 
                                OS DADOS JÁ EXISTENTES PARA EVITAR DUPLICIDADE DE DADOS. O CÓDIGO ABAIXO FAZ ESSA VERIFICAÇÃO DOS DADOS EXISTENTES"""
                                if os.path.exists("insert_dimensao_produto_intermediario.sql"):
                                    with open("insert_dimensao_produto_intermediario.sql", "r", encoding="utf-8") as file:
                                        for linha in file:
                                            # A expressão regular captura os valores entre aspas após VALUES
                                            match = re.search(r"VALUES \('(.+?)', '(.+?)'\);", linha)
                                            if match:
                                                produto, categoria = match.group(1), match.group(2)
                                                produtos_inseridos.add((produto, categoria))

                                # Verificando se a categoria está contida no nome_atual
                                for categoria in categorias:
                                    if categoria in produto_atual.lower():  # Verifica se a categoria é um subconjunto do nome
                                        if(produto_atual, categoria) not in produtos_inseridos: # Verifica se não existe duplicidade de tuplas de iterações anteoriores
                                            insert_statement = f"INSERT INTO {table_name} (nome_produto, cultura_especie) VALUES ('{produto_atual}', '{categoria}');"
                                            insert_statements.append(insert_statement)
                                            produtos_inseridos.add((produto_atual, categoria))

                                # Salvando os INSERTs em um arquivo .txt para insert posterior
                                with open("insert_dimensao_produto_intermediario.sql", "a", encoding="utf-8") as file: 
                                    for statement in insert_statements:
                                        file.write(statement + "\n")

                                insert_statements.clear()  # Limpa a lista de comandos SQL para evitar duplicatas
                                break  # Para na primeira ocorrência                       
                
            # Verifica se o botão de próxima página está presente e habilitado
            finalizar = False # Flag para finalizar o loop principal caso não encontre mais páginas
            while True:
                try:
                    proxima_pagina = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Avançar página']"))
                    )
                    # Verifica se o botão está desabilitado
                    if "disabled" in proxima_pagina.get_attribute("class"):
                        print("Fim das páginas.")
                        finalizar = True
                        break
                    clicar_elemento(By.XPATH, "//button[@aria-label='Avançar página']", descricao="botão de próxima página")
                    break  # Sai do loop se a ação ocorrer com sucesso
                except Exception as e:
                    print("Erro ao acessar o botão de próxima página:", e)  
                    time.sleep(5)
            if finalizar:
                break  # Encerra o loop principal se não houver mais páginas

            # Aguarda um tempo adicional para garantir que a página seja carregada
            time.sleep(4)

            # Aguarda até que a nova página seja carregada
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'tr'))
            )

        except Exception as e:
            print(f"Erro: {e}")
            break

driver.quit()