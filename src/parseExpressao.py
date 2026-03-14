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

    return tokens


def estadoInicial(char, lista, tokens, linha, index):
    if char.isspace(): 
        return estadoInicial, ""

    if char in "()":
        return estadoParenteses(char, lista, tokens, linha, index)

    # Quando ponto, chamar estadoNúmero que irá validar caracter
    if char.isdigit() or char == '.':
        return estadoNumero, char

    # Verificar se menos é subtracao ou negativo
    # Se prox char for numero, menos é parte do número negativo, caso contrário é operador de subtração
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
        return estadoOperador, char

    # Tratativa para erro léxico fatal quando lermos símbolo alienígena ex: ~ ou @ que não seja operador previsto...
    raise ValueError(f"Erro: caractere desconhecido ou não esperado '{char}' na posição {index}")


def estadoNumero(char, lista, tokens, linha, index):
    # Enquanto for vindo número (digito), continuamos crescendo a variável lista que abriga nosso formato numérico
    if char.isdigit():
        return estadoNumero, lista + char

    # Se esbarrarmos num pontinho pra criar um float/double...
    if char == '.':
        # Antes verificamos: se o lista atual JÁ TEM um ponto, colocar mais um geraria dois pontos. E número com dois pontos (ex: 3.14.5) não existe! Da erro!
        if '.' in lista:
            raise ValueError(f"Erro: número malformado na posição {index} gerou múltiplos pontos inválidos (ex: {lista + char})")
        
        # Mas, se não houver um ponto lá ainda, agregamos com sucesso e aceitamos a dízima decimal!
        return estadoNumero, lista + char

    # Se a gente estava num número e esbarrou numa letra ou operador sem ser número nem ponto:
    # Alcançamos a fronteira do número! Ele terminou (por exemplo: um parêntese encostado cortou).
    
    # Mas cuidado: Tratamento breve para número falso que por engano tenha tido apenas um sinal '-' ou só um '.' sem números a frente!
    if lista == '-' or lista == '.':
        raise ValueError(f"Erro: sequência inválida tentando formar número falhou, sobrando apenas um: '{lista}'")
        
    # Salvo raras excessões acima, colocamos o belo número na lista principal do Lexer com sucesso de extração!
    tokens.append(lista)
    
    # IMPORTANTE DA MÁQUINA DE ESTADO: 
    # Precisamos validar de novo qual a função desse CARACTERE NOVO que parou o número, 
    # e fazemos isso repassando no porteiro chefe pra verificar qual seu estado!
    return estadoInicial(char, "", tokens, linha, index)


def estadoOperador(char, lista, tokens, linha, index):
    # O estado operador é versátil, atende matemática e letras do alfabeto (MEM e RES).

    # Se recebemos letras nele, é montagem de palavra.
    if lista.isalpha():
        # Enquanto for chegando letra, é farra! O comando vai crescendo lindamente.
        if char.isalpha():
            return estadoOperador, lista + char
        else:
            # Ops, não é mais letra? Pode ser um final de string. Fechou comando com sucesso!
            # Salvamos ele bonitão gigante maiúsculo (upper) pra ficar chique e limpo em caixa alta na lista!
            tokens.append(lista.upper())
            
            # Repassa a parada do char novato problemático pro inicio lidar
            return estadoInicial(char, "", tokens, linha, index)

    # Se no lista mora uma solitária barra '/' aguardando destino...
    if lista == '/':
        # A letra logo após a barra vai decidir minha salvação
        if char == '/':
             tokens.append('//') # Finalizou Divisão de Inteiros (duas barras) e corre pro abraço
             return estadoInicial, ""
        else:
             # Falso alarme, a próxima era normal... É divisão comum '/' mesmo. Adiciona a barra salva!
             tokens.append('/')
             # E a letrinha enxerida a seguir leva um recomeço em avaliação!
             return estadoInicial(char, "", tokens, linha, index)

    # Se por ventura cheguei aqui zeradinho só na ansiedade inicial dos chars puros vazios:
    if lista == "":
        if char == '/':
            # Aguardamos confirmação de dupla de barras armazenando aqui pra próxima rodada descobrir
            return estadoOperador, char
            
        if char in "+-*^%":
            # Demais operadores são fáceis.. só adicionar instantâneo o solitário deles que ta validado.
            tokens.append(char)
            # Retorna limpo de novo
            return estadoInicial, ""

    # Pra garantir que erros mortais fiquem bem definidos caso o programador mude um estado errado no futuro
    raise ValueError(f"Bizarro erro detectado lendo estado base do char '{char}' ou lista '{lista}' indexado em {index}")


def estadoParenteses(char, lista, tokens, linha, index):
    # Esse estado é puramente instantâneo pra dar respiro em coisas separadas de agrupamento aritmético.
    
    # Pega direto ele sem avaliar lista e guarda nas listas do token!
    tokens.append(char)
    
    # E limpa o estado de comando em branco voltando tudo a normalidade.
    return estadoInicial, ""


def estadoFinal(lista, tokens):
    # Essa função faz a manutenção da varredura, é como limpar o escritório as 18 hrs pós expediente.
    # Serve pro resquício final que a última rodada do While deixou solto.

    # Sem nada pro lixo? Vaza pra casa de boa.
    if not lista:
        return

    # Um restinho deixado de letrinhas (exemplo palavra "RES" que encostava grudada no finalzinho da ponta sem espaço e sobrou).
    if lista.isalpha():
        tokens.append(lista.upper())
        return
        
    # Barra solitária dividida do alem presa até o encerramento puro
    if lista == '/':
        tokens.append('/')
        return
        
    # Segredo barrando pedaços que não valem nem de longe ser inteiros no final das contas '-' ou '.'
    if lista == '-' or lista == '.':
        raise ValueError(f"Encerramento na linha lido em final falso de número pendente e largado: '{lista}'")

    # Passou aí... Tem validação pro final número! Analisamos os bixo, basta verificar se não sobrou nenhuma dízima suja com erro ou etc.
    # Exige no caso concreto, se tiver algum número dentre todas as caracteres da string lista a gente dá confere se ta na regra normalizada base!
    tem_digito = False
    for caractere in lista:
         if caractere.isdigit():
             tem_digito = True
             break
    
    if tem_digito:
        tokens.append(lista)
        return

    # Acusação generalista se alguma tranqueira vazar 
    raise ValueError(f"O item analisado não encaixa se restou para lixo, problema em conteúdo do lixo na saida: '{lista}'")
