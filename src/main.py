#Integrantes: 

#Alexandre Faisst 
#Bruno Teider 
#Luiz Mathias 
#Rafaela Vecchi 
 
# #Grupo RA1 1

import sys
from exibirResultados import ler_arquivo
import parseExpressao


def main(argv=None):
    argv = argv if argv is not None else sys.argv

    if len(argv) < 2:
        print("Uso: python src/main.py <nome_arquivo>")
        sys.exit(1)

    arquivo = argv[1]
    linhas = ler_arquivo(arquivo)

    print("\n=== Analisador Léxico (tokens) ===")
    for idx, linha in enumerate(linhas, start=1):
        if not linha.strip():
            continue

        try:
            tokens = parseExpressao.parseExpressao(linha)
        except Exception as e:
            print(f"Linha {idx}: erro ao analisar: {e}")
            continue

        print(f"Linha {idx}: {linha}")
        print(f"Tokens: {tokens}\n")


if __name__ == "__main__":
    main()