from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acessa a página do IBGE
driver.get('https://www.ibge.gov.br/explica/codigos-dos-municipios.php')

# Aguarda o carregamento da página
time.sleep(5)  # Ajuste o tempo conforme necessário

# Lista para armazenar os nomes das cidades com a UF
cidades_com_uf = []

# Encontra todas as tabelas de municípios
tabelas = driver.find_elements(By.CSS_SELECTOR, "tbody.codigos-list")

# Itera sobre as tabelas e coleta os nomes das cidades com a UF
for tabela in tabelas:
    # Encontra o <thead> anterior à tabela atual para obter a UF
    thead = tabela.find_element(By.XPATH, "./preceding-sibling::thead[1]")
    uf = thead.get_attribute("id")  # O ID do <thead> é a sigla da UF
    
    # Itera sobre as linhas da tabela para coletar os nomes das cidades
    linhas = tabela.find_elements(By.CSS_SELECTOR, "tr.municipio.data-line")
    for linha in linhas:
        cidade = linha.find_element(By.CSS_SELECTOR, "td > a").text
        cidades_com_uf.append(f"{uf}_{cidade}")

# Fecha o navegador
driver.quit()

# Exibe os nomes das cidades com a UF
for cidade_uf in cidades_com_uf:
    print(cidade_uf)

# Salva os nomes das cidades com a UF em um arquivo (opcional)
with open("cidades_ibge_com_uf.txt", "w") as arquivo:
    for cidade_uf in cidades_com_uf:
        arquivo.write(cidade_uf + "\n")