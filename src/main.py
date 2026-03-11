#Integrantes: 

#Alexandre Faisst 
#Bruno Teider 
#Luiz Mathias 
#Rafaela Vecchi 
 
# #Grupo RA1 1

import sys
from exibirResultados import ler_arquivo


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/main.py <nome_arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]
    linhas = ler_arquivo(arquivo)