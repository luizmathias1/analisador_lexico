# Exemplo de fluxo: 4.2 1.0 +
# Lê número 4.2, entra no estado número, recebe o ponto, continua no estado número, recebe o 2, continua no estado número, 
# recebe o espaço, sai do estado número e salva o token "4.2", volta pro estado inicial, recebe o 1, entra no estado número, 
# recebe o ponto, continua no estado número, recebe o 0, continua no estado número, recebe o espaço, sai do estado número e 
# salva o token "1.0", volta pro estado inicial, recebe o +, reconhece como operador e salva o token "+", volta pro estado inicial 
# e termina a leitura da linha.

# -- Informações para Debug --
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def printEstado(state_name, char, lista, index, color):
    print(f"{color}[{state_name}] index={index} char={repr(char)} lista={repr(lista)}{RESET}")

def printTokenConcluido(tokens):
    print(f"{GREEN}lista concluida -> tokens: {tokens}{RESET}")

# -- Execução principal --

def parseExpressao(linha):
    tokens = []
    if not isinstance(linha, str): raise TypeError("parseExpressao espera uma string como 'linha'")

    linha = linha.strip()
    if not linha: return tokens

    estado = estadoInicial
    lista = ""
    index = 0
    
    while index < len(linha):
        char = linha[index]
        estado, lista = estado(char, lista, tokens, linha, index)
        index += 1

    return estadoFinal(tokens)

def estadoInicial(char, lista, tokens, linha, index):
    printEstado("estadoInicial", char, lista, index, BLUE)
    if char.isspace(): 
        return estadoInicial, ""

    if char in "()":
        return estadoParenteses(char, lista, tokens, linha, index)

    # Quando ponto, estadoNúmero que irá validar caracter
    if char.isdigit() or char == '.':
        return estadoNumero, char

    # Verifica se menos é subtração ou negativo, checando proximo char
    if char == '-':
        prox = linha[index + 1] if index + 1 < len(linha) else ''
        
        if prox.isdigit():
            return estadoNumero, char
        else:
            return estadoOperador(char, lista, tokens, linha, index)

    # Tratamento de operadores
    if char in "+*/^%":
        return estadoOperador(char, lista, tokens, linha, index)

    # As letras formam os comandos especiais (RES) ou variveis de memória (MEM, X, Y)
    if char.isalpha():
        return estadoComando, char

    raise ValueError(f"Erro: caractere desconhecido ou não esperado '{char}' na posição {index}")

def estadoNumero(char, lista, tokens, linha, index):
    printEstado("estadoNumero", char, lista, index, CYAN)
    # Enquanto recebemos numeros decimais, chamamos recursimente
    if char.isdigit():
        return estadoNumero, lista + char

    # checar se é dois pontos seguidos, se não for chama a função recursivamente
    if char == '.':
        if '.' in lista:
            raise ValueError(f"Erro: número malformado na posição {index} gerou múltiplos pontos inválidos (ex: {lista + char})")
        else:
            return estadoNumero, lista + char
    
    # Caso receba uma letra, identifica que é um comando
    if char.isalpha():
        return estadoComando, lista + char

    # Verificação de segurança: evita salvar lixo como número
    if lista == '-' or lista == '.':
        raise ValueError(f"Erro: sequência inválida tentando formar número falhou, sobrando apenas um: '{lista}'")
        
    # Salvar o número completo na lista de tokens, já que o próximo char não é mais parte do número
    tokens.append(lista)
    printTokenConcluido(tokens)
    
    # Repassa o caractere atual pro estado inicial, assim comecando uma nova lista
    return estadoInicial(char, "", tokens, linha, index)

def estadoComando(char, lista, tokens, linha, index):
    printEstado("estadoComando", char, lista, index, MAGENTA)
    if lista.isalpha():
        # Enquanto letra, continua recursivamente
        if char.isalpha():
            return estadoComando, lista + char
        else:
            # Caso nao seja mais letra, salvar o comando 
            tokens.append(lista)
            printTokenConcluido(tokens)
            return estadoInicial(char, "", tokens, linha, index)

def estadoOperador(char, lista, tokens, linha, index):
    printEstado("estadoOperador", char, lista, index, YELLOW)
    # Checar divisão inteira
    if lista == '/':
        if char == '/':
             tokens.append('//') 
             printTokenConcluido(tokens)
             return estadoInicial, ""
        else:
             # Caso não seja, salva divisao real
             tokens.append('/')
             printTokenConcluido(tokens)
             return estadoInicial(char, "", tokens, linha, index)

    if lista == "":
        if char == '/':
            # Chama recursivamente para checar divisão inteira
            return estadoOperador, char
            
        # Demais operadores
        if char in "+-*^%":
            tokens.append(char)
            printTokenConcluido(tokens)
            return estadoInicial, ""

    raise ValueError(f"Erro: erro lendo '{char}' ou lista '{lista}' indexado em {index}")

#URGENTE  Refatorar estadoParenteses não está funcionando corretamente
#exemplo: (( sem ser fechado 
def estadoParenteses(char, lista, tokens, linha, index):
    printEstado("estadoParenteses", char, lista, index, WHITE)
    
    # Pega direto ele sem avaliar lista e guarda nas listas do token!
    tokens.append(char)
    printTokenConcluido(tokens)
    
    # E limpa o estado de comando em branco voltando tudo a normalidade.
    return estadoInicial, ""

def estadoFinal(tokens):
    if not tokens:
        raise ValueError("Erro: expressão vazia ou malformada, nenhum token reconhecido")

    print('Gerando JSON dos tokens...')

    return tokens