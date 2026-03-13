# Alertar se o arquivo tiver linhas malformadas ou exceder limites.
import parseExpressao

def ler_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    print(f"Arquivo '{arquivo}' lido com sucesso. Total de linhas: {len(linhas)}")

    formatado = []
    for linha in linhas:
        formatado.append(linha.strip("\n"))

    return formatado

