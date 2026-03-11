# Alertar se o arquivo tiver linhas malformadas ou exceder limites.

def ler_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    for i, linha in enumerate(linhas):
        if len(linha) > 200:
            raise ValueError(f"Erro: Linha {i+1} excede o limite de 200 caracteres.")
    
    print(f"Arquivo '{arquivo}' lido com sucesso. Total de linhas: {len(linhas)}")

    formatado = []
    for linha in linhas:
        formatado.append(linha.strip("\n"))

    print(formatado)
    return formatado
