import subprocess
import os

def compactar_rar(pasta = "pdfs", nome_rar: str = "arquivos_comprimidos.rar"):
    os.makedirs(pasta, exist_ok=True)

    winrar_path = r"C:\Program Files\WinRAR\WinRAR.exe"

    comando = [winrar_path, "a", "-r", nome_rar, "*.*"]

    try:
        subprocess.run(comando, cwd=pasta, check=True)
        return f"Arquivos compactados em RAR: {pasta, nome_rar}"
    except Exception as e:
        return f" Erro ao compactar em RAR {e}"