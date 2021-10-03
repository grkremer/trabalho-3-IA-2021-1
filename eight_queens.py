import random

def verifica_linha(x, individual):
    ataques = 0
    
    for i in range(len(individual)):
        if i != x and individual[i] == individual[x]:
            ataques += 1
    
    return ataques

def verifica_diagonal(x, individual):
    ataques = 0
    
    # sentido / baixo
    y = individual[x]-1
    xNovo = x-1
    while (xNovo >= 0 and y > 0):
        if individual[xNovo] == y:
            ataques +=1
        y -= 1
        xNovo -=1

    # sentido / cima
    y = individual[x]+1
    xNovo = x+1
    while (xNovo < len(individual) and y < len(individual)+1):
        if individual[xNovo] == y:
            ataques +=1
        y += 1
        xNovo +=1

    # sentido \ cima
    y = individual[x]+1
    xNovo = x-1
    while (xNovo > 0 and y < len(individual)+1):
        if individual[xNovo] == y:
            ataques +=1
        y += 1
        xNovo -=1

    # sentido \ baixo
    y = individual[x]-1
    xNovo = x+1
    while (xNovo < len(individual) and y > 0):
        if individual[xNovo] == y:
            ataques +=1
        y -= 1
        xNovo +=1

    return ataques

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    total_ataques = 0

    for x in range(len(individual)):
        total_ataques += verifica_linha(x, individual)
        total_ataques += verifica_diagonal(x, individual)
    
    return total_ataques/2


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    melhor_inividuo = participants[0]
    melhor_conflitos = 10000

    for individuo in participants:
        conflitos = evaluate(individuo)
        if conflitos < melhor_conflitos:
            melhor_inividuo = individuo
            melhor_conflitos = conflitos

    return melhor_inividuo


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    final1 = parent1[index:]
    final2 = parent2[index:]
    filho1 = parent1[:index]
    filho1 += final2
    filho2 = parent2[:index]
    filho2 += final1

    return filho1, filho2


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random.random() < m:
        sorteio = random.randint(0, len(individual)-1)
        individual[sorteio] = random.randint(1,8)
    
    return individual


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """
    #1 Gera n individuos
    individuos = [None]*n
    for i in range(len(individuos)):
        novo_individuo = [None]*8
        for j in range(len(novo_individuo)):
            novo_individuo[j] = random.randint(1,8)
        individuos[i] = novo_individuo
        
    melhor_individuo = tournament(individuos)
    for geração in range(g):
        #1.1 Muta os n individuos
        for i in range(len(individuos)-1):
            individuos[i] = mutate(melhor_individuo, m)
    
        #2 Avalia os n individuos
        #3 ordena com base na pontuação
        melhor_individuo = tournament(individuos)
        
        # Se tem elitismo...
        if e:
            individuos.remove(melhor_individuo)
            segundo_melhor = tournament(individuos)
            index = random.randint(0, len(melhor_individuo)-1)
            melhor_individuo, segundo_melhor = crossover(melhor_individuo, segundo_melhor, index)
            individuos.append(melhor_individuo)
        print(evaluate(melhor_individuo))
    
    return melhor_individuo


if __name__ == "__main__":
    #melhor_individuo = run_ga(100, 40, 2, 0.3, True)
    melhor_individuo = run_ga(3, 5, 2, 0.3, False)
    print(melhor_individuo)
    #print(evaluate(melhor_individuo))