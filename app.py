import requests
import re
from bs4 import BeautifulSoup

def obtener_enlace_m3u8(url):
    try:
        # Configurar encabezados para simular un navegador
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": url,
        }

        # Realizar la solicitud inicial a la página
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error al acceder a la página: {response.status_code}"

        # Analizar el contenido HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar scripts que puedan contener el enlace .m3u8
        scripts = soup.find_all("script")
        m3u8_pattern = re.compile(r'https://[^\s]*\.m3u8[^\s]*')
        enlace_m3u8 = None

        for script in scripts:
            if script.string:
                match = m3u8_pattern.search(script.string)
                if match:
                    enlace_m3u8 = match.group(0)
                    break

        # Si no se encuentra el enlace en los scripts, buscar en las solicitudes AJAX
        if not enlace_m3u8:
            # Extraer posibles endpoints AJAX desde el HTML
            ajax_endpoints = re.findall(r'"(https?://[^"]+)"', response.text)
            for endpoint in ajax_endpoints:
                try:
                    ajax_response = requests.get(endpoint, headers=headers)
                    if ajax_response.status_code == 200:
                        match = m3u8_pattern.search(ajax_response.text)
                        if match:
                            enlace_m3u8 = match.group(0)
                            break
                except Exception as e:
                    continue

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
