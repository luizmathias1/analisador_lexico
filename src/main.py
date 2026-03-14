#Integrantes: 

#Alexandre Faisst 
#Bruno Teider 
#Luiz Mathias 
#Rafaela Vecchi 
 
# #Grupo RA1 1

import json
import os
import sys
from exibirResultados import ler_arquivo
import parseExpressao

def resetJson():
    output_path = os.path.join("results", "tokens.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # garante que 'results/' exista
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"entries": []}, f, ensure_ascii=False, indent=2)

def main(argv=None):
    argv = argv if argv is not None else sys.argv

    if len(argv) < 2:
        print("Uso: python src/main.py <nome_arquivo>")
        sys.exit(1)

    try:
        arquivo = argv[1]
        linhas = ler_arquivo(arquivo)
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
        sys.exit(1)

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
    resetJson() # Garantir que sempre começamos com um JSON vazio
    main()