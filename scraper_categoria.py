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
nomes_produtos = [] # Armazena os nomes dos produtos

driver.get('https://consultaprecosdemercado.conab.gov.br/#/home')
time.sleep(2)

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

# Selecionando botão Pesquisar 
botao_pesquisar = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
botao_pesquisar.click()
time.sleep(2)

# Selecionando a categoria
categoria_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "produto")))
categoria_dropdown.click()
elementos = driver.find_elements(By.CSS_SELECTOR, ".br-item label")

for elemento in elementos:
    if elemento.text == '' or elemento.text == 'Selecionar Todos' or elemento.text == '10-30-15':
        continue
    nomes_produtos.append(elemento.text)

# Selecionar o mês inicial (Janeiro)
mes_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesInicial")))
mes_inicial_dropdown.click()
mes_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesInicial0']")))  # Janeiro
mes_inicial.click()

# Selecionar o ano inicial (2018)
ano_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoInicial")))
ano_inicial_dropdown.click()
ano_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoInicial7']")))  # 2018
ano_inicial.click()

# Selecionar o mês final (Dezembro)
mes_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesFinal")))
mes_final_dropdown.click()
mes_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesFinal11']")))  # Dezembro
mes_final.click()

# Selecionar o ano final (2021)
ano_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoFinal")))
ano_final_dropdown.click()
ano_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoFinal4']")))  # 2021
ano_final.click()

# Selecionando botão Pesquisar 
botao_pesquisar = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
botao_pesquisar.click()
time.sleep(2)

# Selecionando a categoria
categoria_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "produto")))
categoria_dropdown.click()
elementos = driver.find_elements(By.CSS_SELECTOR, ".br-item label")

for elemento in elementos:
    if elemento.text == '' or elemento.text == 'Selecionar Todos' or elemento.text in nomes_produtos or elemento.text == '10-30-15':
        continue
    nomes_produtos.append(elemento.text)

# Selecionar o mês inicial (Janeiro)
mes_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesInicial")))
mes_inicial_dropdown.click()
mes_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesInicial0']")))  # Janeiro
mes_inicial.click()

# Selecionar o ano inicial (2022)
ano_inicial_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoInicial")))
ano_inicial_dropdown.click()
ano_inicial = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoInicial3']")))  # 2022
ano_inicial.click()

# Selecionar o mês final (Janeiro)
mes_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mesFinal")))
mes_final_dropdown.click()
mes_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mesFinal0']")))  # Dezembro
mes_final.click()

# Selecionar o ano final (2025)
ano_final_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "anoFinal")))
ano_final_dropdown.click()
ano_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='anoFinal0']")))  # 2025
ano_final.click()

# Selecionando botão Pesquisar 
botao_pesquisar = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
botao_pesquisar.click()
time.sleep(2)

# Selecionando a categoria
categoria_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "produto")))
categoria_dropdown.click()
elementos = driver.find_elements(By.CSS_SELECTOR, ".br-item label")

for elemento in elementos:
    if (elemento.text == '' or elemento.text == 'Selecionar Todos' or elemento.text in nomes_produtos) or elemento.text == '10-30-15':
        continue
    nomes_produtos.append(elemento.text)

nomes_produtos.sort()

with open("categoria.txt", "w", encoding="utf-8") as arquivo:
    for produto in nomes_produtos:
        arquivo.write(produto + "\n")

driver.quit()