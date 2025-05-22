import requests
from bs4 import BeautifulSoup

def buscar_productos(palabra="laptop"):
    url = f"https://listado.mercadolibre.com.co/{palabra}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    print("Response: ", response)
    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("li.ui-search-layout__item")[:5]
    for i, prod in enumerate(productos, 1):
        titulo = prod.select_one("a.poly-component__title")
        precio = prod.select_one("div.poly-price__current span.andes-money-amount__fraction")
        print(f"{i}. {titulo.text if titulo else 'Sin título'} - ${precio.text if precio else 'Sin precio'}")

# Ejecutar búsqueda
buscar_productos("Carros")
