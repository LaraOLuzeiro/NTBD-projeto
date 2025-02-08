import time
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
time.sleep(3)
print(driver.title) # Título da página

# Seleciona preços mensais
botao_preco_mensal = driver.find_element(By.XPATH, "//button[.//i[contains(@class, 'fa-th-large')]]")
botao_preco_mensal.click()

# Selecionar o mês inicial (Janeiro)
mes_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesInicial")))
mes_inicial_dropdown.click()
mes_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesInicial0']")))  # Janeiro
mes_inicial.click()

# Selecionar o ano inicial (2014)
ano_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoInicial")))
ano_inicial_dropdown.click()
ano_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoInicial11']")))  # 2014
ano_inicial.click()

# Selecionar o mês final (Dezembro)
mes_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesFinal")))
mes_final_dropdown.click()
mes_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesFinal11']")))  # Dezembro
mes_final.click()

# Selecionar o ano final (2017)
ano_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoFinal")))
ano_final_dropdown.click()
ano_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoFinal8']")))  # 2017
ano_final.click()

# Selecionando botões Pesquisar e Consultar
botao_pesquisar = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
botao_pesquisar.click()
time.sleep(3)
botao_consultar = driver.find_element(By.XPATH, "//button[contains(text(), 'Consultar')]")
botao_consultar.click()

# Selecionando máximo de 100 resultados por página (nao funciona)
# botao_selecao = driver.find_element(By.XPATH, "//button[@aria-label='Exibir lista']")
# botao_selecao_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-trigger='data-trigger']")))
# botao_selecao_dropdown.click()
# botao_selecao = wait.until(EC.element_to_be_clickable((By.ID, "per-page-selection-random5")))
# botao_selecao.click()

contador = 2 # Número da próxima página

with open("produtos.txt", "w") as arquivo:
    while True:
        try:
            # Aguarda até que os resultados estejam presentes na página
            WebDriverWait(driver, 10).until( # Aguarda 10 segundos no máximo até dar erro de timeout
                EC.presence_of_element_located((By.TAG_NAME, 'tr'))  # Verifica se o elento <tr> está presente no DOM, dentro dos 10 seg
            )

            time.sleep(5)
            
            resultados = driver.find_elements(By.TAG_NAME, 'tr')

            for resultado in resultados:
                arquivo.write(resultado.text + "\n")

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
            except Exception as e:
                print("Botão de próxima página não encontrado:", e)
                break

            # Chama a função JavaScript diretamente
            driver.execute_script(f"navigateToPage('frmFiltroGeral-5231', '{contador}');")

            # Aguarda um tempo adicional para garantir que a página seja carregada
            time.sleep(5)  # Reduzi o tempo de espera para 2 segundos para fins de teste

            # Aguarda até que a nova página seja carregada
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'tr'))
            )

            contador += 1

        except Exception as e:
            print("Erro:", e)
            break

driver.quit()