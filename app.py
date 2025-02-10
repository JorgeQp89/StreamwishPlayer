from playwright.sync_api import sync_playwright
import re

def obtener_enlace_m3u8(url):
    try:
        with sync_playwright() as p:
            # Iniciar un navegador Chromium en modo headless
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navegar a la URL
            page.goto(url, wait_until="networkidle")

            # Esperar a que el elemento <video> esté presente
            page.wait_for_selector("video", timeout=20000)

            # Capturar el tráfico de red
            m3u8_pattern = re.compile(r'https://[^\s]*\.m3u8[^\s]*')
            enlace_m3u8 = None

            def handle_request(route, request):
                nonlocal enlace_m3u8
                if ".m3u8" in request.url:
                    enlace_m3u8 = request.url
                route.continue_()

            # Intercepta las solicitudes de red
            page.route("**/*.m3u8", handle_request)

            # Simular la reproducción del video
            page.evaluate("document.querySelector('video').play()")

            # Esperar unos segundos para capturar el tráfico
            page.wait_for_timeout(5000)

            # Cerrar el navegador
            browser.close()

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
