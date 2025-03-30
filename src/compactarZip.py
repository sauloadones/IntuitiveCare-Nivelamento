import os
import zipfile
def compactar_em_zip(pasta = "pdfs", nome_zip: str = "arquivos_comprimidos.zip"):
    os.makedirs(pasta, exist_ok=True)
    caminho_zip = os.path.join(pasta, nome_zip)
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pasta):
            for arquivo in files:
                if arquivo != nome_zip:
                    caminho_arquivo = os.path.join(root, arquivo)
                    zipf.write(caminho_arquivo, arcname=arquivo)

