import pandas as pd
from pathlib import Path
def renomear_colunas(coluna: str, coluna_renomeada: str, nome_arquivo: str):
    import pandas as pd
    from pathlib import Path

    def limpar_nome_colunas(df):
        df.columns = [col.replace('\n', ' ').strip() for col in df.columns]
        return df

    base_dir = Path(__file__).resolve().parent
    caminho = base_dir.parent / "csvs" / f"{nome_arquivo}.csv"

    df = pd.read_csv(caminho)
    df = limpar_nome_colunas(df)

    print("Colunas disponíveis:", df.columns.tolist())

    if coluna not in df.columns:
        print(f" A coluna '{coluna}' não foi encontrada exatamente.")
        return

    df.rename(columns={coluna: coluna_renomeada}, inplace=True)

    saida = base_dir.parent / "csvs" / f"{nome_arquivo}_renomeado.csv"
    df.to_csv(saida, index=False)
    print(f" Coluna '{coluna}' renomeada para '{coluna_renomeada}'. Arquivo salvo em: {saida}")



def usuarioRenomea():
    nome_arquivo = input("Qual o arquivo que voce quer renomear")
    resposta = True
    while resposta == True:
        nome = input("Digite o nome da coluna para ser renomeada")
        troca_de_nome = input("Qual vai ser o novo nome da coluna")
        mostrar_colunas(f"{nome_arquivo}_renomeado")
        renomear_colunas(nome, troca_de_nome, nome_arquivo)
        resposta = input("Deseja renomear mais alguma tabela")
        if resposta.lower() != "sim":
            print("Encerrando renomeação")
            break


def mostrar_colunas(nome_arquivo):
    base_dir = Path(__file__).resolve().parent
    caminho = base_dir.parent / "csvs" / f"{nome_arquivo}.csv"
    df = pd.read_csv(caminho)
    
    print("\n🧾 Cabeçalho real do arquivo CSV:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. '{col}'")

