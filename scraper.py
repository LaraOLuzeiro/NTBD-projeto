# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from PIL import Image
# import pytesseract
# import requests
# from io import BytesIO

# # Função para extrair texto de uma imagem usando OCR
# def extrair_texto_da_imagem(url_imagem):
#     response = requests.get(url_imagem)
#     img = Image.open(BytesIO(response.content))
#     texto = pytesseract.image_to_string(img)
#     return texto.strip()

# # Inicializa o WebDriver com o webdriver_manager
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# driver.get('https://www.agrolink.com.br/cotacoes/busca/')
# print(driver.title)

# while True:
#     try:
#         # Aguarda até que os resultados estejam presentes na página
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, 'tr'))
#         )
        
#         resultados = driver.find_elements(By.TAG_NAME, 'tr')
#         for resultado in resultados:
#             # Supondo que a imagem do preço esteja em uma tag <img> dentro da linha
#             try:
#                 img_preco = resultado.find_element(By.TAG_NAME, 'img')
#                 url_imagem = img_preco.get_attribute('src')
#                 preco = extrair_texto_da_imagem(url_imagem)
#                 print(f"Preço extraído: {preco}")
#             except:
#                 print("Imagem do preço não encontrada.")
#                 continue

#         # Verifica se o botão de próxima página está presente e habilitado
#         try:
#             proxima_pagina = driver.find_element(By.CLASS_NAME, 'btn-navigation btn-navigation-next')
#             if "disabled" in proxima_pagina.get_attribute("class"):
#                 print("Fim das páginas.")
#                 break
#         except:
#             print("Botão de próxima página não encontrado.")
#             break

#         # Clica no botão de próxima página
#         proxima_pagina.click()

#         # Aguarda um tempo adicional para garantir que a página seja carregada
#         time.sleep(1000)

#         # Aguarda até que a nova página seja carregada
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, 'tr'))
#         )

#     except Exception as e:
#         print("Erro:", e)
#         break

# driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa o WebDriver com o webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.agrolink.com.br/cotacoes/busca/')
time.sleep(5)
print(driver.title)

link_login = driver.find_element(By.CLASS_NAME, "header-link.has-icon.align-middle.cor-branco")
link_login.click()
time.sleep(5)

# Localiza os campos de login e senha dentro do modal
campo_usuario = driver.find_element(By.ID, "NomeUsuarioLogin")  
campo_senha = driver.find_element(By.ID, "SenhaLogin")  

# Preenche os campos e clica no botão de login
campo_usuario.send_keys("loluzeiro@estudante.ufscar.br")
campo_senha.send_keys("senha12345")
botao_login = driver.find_element(By.CLASS_NAME, "btn.btn-light-green.btn-form")     
botao_login.click()
time.sleep(3)

contador = 2 # Número da próxima página

with open("produtos.txt", "w") as arquivo:
    while True:
        try:
            # Aguarda até que os resultados estejam presentes na página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'tr'))
            )

            time.sleep(5)
            
            resultados = driver.find_elements(By.TAG_NAME, 'tr')

            for resultado in resultados:
                arquivo.write(resultado.text + "\n")

            # Verifica se o botão de próxima página está presente e habilitado
            try:
                # Localiza o botão de próxima página pelo XPath
                proxima_pagina = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='btn-navigation btn-navigation-next' and contains(@href, 'javascript:navigateToPage')]"))
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