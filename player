import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def obtener_enlace_m3u8(url):
    try:
        # Configuración de Selenium con Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")  # Reducir mensajes de registro

        # Inicializar el controlador de Chrome
        service = Service("chromedriver")  # Asegúrate de tener chromedriver instalado
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Abrir la página de StreamWish
        driver.get(url)

        # Esperar a que el reproductor cargue completamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        # Simular la reproducción del video
        video_element = driver.find_element(By.TAG_NAME, "video")
        driver.execute_script("arguments[0].play();", video_element)

        # Esperar unos segundos para que se genere el tráfico de red
        time.sleep(5)

        # Capturar las solicitudes de red
        logs = driver.get_log("performance")
        m3u8_pattern = re.compile(r'https://[^\s]*\.m3u8[^\s]*')

        enlace_m3u8 = None
        for log in logs:
            message = log["message"]
            if "Network.requestWillBeSent" in message:
                match = m3u8_pattern.search(message)
                if match:
                    enlace_m3u8 = match.group(0)
                    break

        # Cerrar el navegador
        driver.quit()

        if enlace_m3u8:
            return enlace_m3u8
        else:
            return "No se encontró ningún enlace .m3u8 en el tráfico de red."

    except Exception as e:
        return f"Ocurrió un error: {e}"

# Ejemplo de uso
url_streamwish = "https://streamwish.to/e/ycvwokf2eerf"
enlace_original = obtener_enlace_m3u8(url_streamwish)

if enlace_original:
    print(f"Enlace original obtenido: {enlace_original}")
else:
    print("No se pudo obtener el enlace original.")
