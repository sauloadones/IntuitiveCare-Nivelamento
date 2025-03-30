import pdfplumber
import csv
from pathlib import Path
import os
from src.compactarZip import compactar_em_zip
def pdf_to_csv(name: str, nome_arquivo: str):
    # Diretórios
    base_dir = Path(__file__).resolve().parent
    pdf_path = base_dir.parent / "pdfs" / name
    csv_dir = base_dir.parent / "csvs"
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = csv_dir / f"{nome_arquivo}.csv"
    cabecalho_salvo = None

    with pdfplumber.open(pdf_path) as pdf:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for i, page in enumerate(pdf.pages):
                print(f"Processando página {i+1}...")
                table = page.extract_table()
                if table:
                    for row in table:
                    
                        row = [cell.strip() if cell else "" for cell in row]

                        if not any(row):
                            continue

             
                        if cabecalho_salvo is None:
                            cabecalho_salvo = row
                            writer.writerow(row)
                        elif row != cabecalho_salvo:
                            writer.writerow(row)

def escolha_pdf():
    base_dir = Path(__file__).resolve().parent
    pasta = base_dir.parent / "pdfs"

    arquivos_pdf = list(pasta.glob("*.pdf"))

    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return None

    print("Selecione um arquivo PDF:")
    for i, pdf in enumerate(arquivos_pdf, 1):
        print(f"{i}. {pdf.name}")

    while True:
        try:
            nome = input("Digite o nome para colocar no arquivo ao ser transformado")
            escolha = int(input("Digite o número do arquivo desejado: "))
            comp = input("Deseja compactar o arquivo?")
            if comp.lower() == "sim":
                nome_comp = input("Qual o nome do arquivo compactado")
            if 1 <= escolha <= len(arquivos_pdf):
                arquivo_escolhido = arquivos_pdf[escolha - 1]
                print(f"Você escolheu: {arquivo_escolhido.name}")
                pdf_to_csv(arquivo_escolhido, nome)
                if comp.lower() == "sim":
                    print("Compactando Arquivo")
                    compactar_em_zip("csvs", nome_comp)
                return arquivo_escolhido
             
            else:
                print("Numero fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um numero.")





    