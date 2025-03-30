import requests 
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import os


def download_file(*urls, destino = "pdfs"):
    os.makedirs(destino, exist_ok=True)
    for url in urls:
        nome_arquivo = os.path.basename(url)
        caminho_arquivo = os.path.join(destino, nome_arquivo)
        try: 
            resposta = requests.get(url, stream=True)
            resposta.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar{nome}: {e}")
            continue

        with open(caminho_arquivo, 'wb') as f:
            for chunk in resposta.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Salvo em caminho: {caminho_arquivo}")

