import requests 
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import os

import re

def matchWord(texto_link: str, nomes_arquivo: list) -> bool:
    for nome in nomes_arquivo:
        padrao = rf"\b{re.escape(nome.lower())}\b"
        if re.search(padrao, texto_link):
            return True
    return False



def encontrar_arquivos_para_download(url: str, extensao: str, *palavras_chaves):
    # extensao = next((palavra.lower() for palavra in palavras_chaves if palavra.startswith(".")))
    # nomes_arquivos = [palavra.lower() for palavra in palavras_chaves if not palavra.startswith(".")]


    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    arquivos_encontrados = []

    for link in soup.find_all("a", href=True):
        texto = link.get_text(strip=True).lower()
        href=link["href"]
        href_lower = href.lower()
        if (href_lower.endswith(extensao.lower())):
            
            if matchWord(texto, palavras_chaves):
                url_completo = urljoin(url, href)
                arquivos_encontrados.append(url_completo)
    
    return arquivos_encontrados