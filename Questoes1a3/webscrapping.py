import requests
from Questoes1a3.downloadFile import  download_file
from Questoes1a3.buscarArquivo import encontrar_arquivos_para_download
from Questoes1a3.compactarZip import compactar_em_zip
from Questoes1a3.compactarRar import compactar_rar
url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

lista_arquivos = []

def ws():
    url_base = input(("Qual é a url do site que voce deseja baixar os arquivos"))
    pinpoint = True;
    while pinpoint == True:
        arquivos = input("Nome do arquivo a ser baixado")

        confirmacao = input("Deseja baixar mais um arquivo \n SIM OU NÃO")

        lista_arquivos.append(arquivos)

        if confirmacao.lower() == "sim":      
             pinpoint = True
        
        else:
            pinpoint = False
    
    extensao = input("Qual a extensão do arquivo")

    arquivos_encontrados = encontrar_arquivos_para_download(url_base, f".{extensao}", *lista_arquivos) 
    
    download_file(*arquivos_encontrados)

    tipo = input(("Voce deseja compactar em que tipo de formato ESCOLHA ENTRE: RAR ou ZIP"))

    if tipo.lower() == 'rar':
        compactar_rar("pdfs" ,nome_rar="anexos_rar.rar")

    elif tipo.lower() == "zip":
        compactar_em_zip("pdfs" ,nome_zip="anexos_rol.zip")

    else: 
        return "Digite uma formatação valida"