def parseExpressao(linha):
    tokens = []

    if not isinstance(linha, str):
        raise TypeError("parseExpressao espera uma string como 'linha'")

    linha = linha.strip()
    if not linha:
        return tokens

    operadores = {'+', '-', '*', '/', '^', '%', '//'}
    partes = linha.split()

    # Faz o pré-processamento para lidar com parênteses colados a números ou operadores
    for char in partes:
        while char.startswith('('):
            tokens.append('(')
            char = char[1:]

        # conta parênteses de fechamento no final
        trail = 0
        while char.endswith(')') and len(char) > 0:
            trail += 1
            char = char[:-1]

        if char != '':
            if char in operadores:
                tokens.append(char)
            elif is_numero_valido(char):
                tokens.append(char)
            else:
                raise ValueError(f"Erro: Token inválido '{char}'")

        for _ in range(trail):
            tokens.append(')')

    # verifica se o primeiro token significativo é operador
    for t in tokens:
        if t == '(':
            continue
        if t in operadores:
            raise ValueError(f"Erro: Expressão começa com operador '{t}'")
        break

    return tokens

def is_numero_valido(token):
    try:
        float(token)
        if token.startswith('.'):
            return False
        return True
    except ValueError:
        return False

def estadoNumero(token):
    print(f"Processando número: {token}")

def estadoOperador(token):
    print(f"Processando operador: {token}")

def estadoParenteses(token):
    print(f"Processando parênteses: {token}")

