import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def ejecutar_fichaje():
    chrome_options = Options()
    # ACTIVAR HEADLESS PARA GITHUB ACTIONS (Para probar en tu PC, ponlo en False)
    es_github = os.environ.get('GITHUB_ACTIONS') == 'true'
    if es_github:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # Usar variables de entorno (Secrets de GitHub) o tus datos locales
        # user = os.environ.get('USER_PVCAT', 'test')
        # password = os.environ.get('PASS_PVCAT', 'test')

        user = os.environ.get('USER_PVCAT')
        password = os.environ.get('PASS_PVCAT')

        if not user or not password:
            raise ValueError("Missing credentials! Make sure USER_PVCAT and PASS_PVCAT are set in GitHub Secrets.")

        print("Abriendo PVCat...")
        driver.get("https://hora.pvcat.com/login")

        # 1. Login
        print("Introduciendo credenciales...")
        wait.until(EC.presence_of_element_located((By.ID, "inputEmail"))).send_keys(user)
        driver.find_element(By.ID, "inputPassword").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 2. Localizar botón principal de fichaje
        print("Esperando al botón de fichaje...")
        boton_fichar = wait.until(EC.element_to_be_clickable((By.ID, "checkBtn")))

        # 3. Identificar acción (Entrar o Salir)
        clase_boton = boton_fichar.get_attribute("class")
        accion = "ENTRADA" if "btn-success" in clase_boton else "SALIDA"
        print(f"Detectado: Botón de {accion}.")

        # 4. PRIMER CLIC (Abre el mensaje de confirmación)
        boton_fichar.click()
        print("Abriendo confirmación...")

        # 5. SEGUNDO CLIC (Confirmar en el modal 'Si')
        # Esperamos a que el botón '.bootbox-accept' sea visible y clicable
        boton_confirmar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bootbox-accept")))
        boton_confirmar.click()
        
        print(f"¡{accion} confirmada con éxito!")
        time.sleep(5) # Pausa para que la web guarde los datos

    except Exception as e:
        print(f"Error durante el proceso: {e}")
        if not es_github:
            input("Presiona Enter para cerrar y ver el error...")
    finally:
        driver.quit()

if __name__ == "__main__":
    ejecutar_fichaje()