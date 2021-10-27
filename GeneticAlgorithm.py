import networkx as nx
import numpy

def AtualizaPopulacao(grafo, populacao, tamanho_populacao):
    nova_populacao = []

    nova_populacao = Ordena(grafo, populacao)

    for i in range(len(nova_populacao)):
        if i >= tamanho_populacao:
            nova_populacao.pop()
    
    return nova_populacao


def Ordena(grafo, populacao):
    fitness = []
    populacao_ordenada = []

    fitness = Fitness(grafo, populacao)

    for i  in range(len(populacao)):
        populacao[i].append(fitness[i])

    populacao_ordenada = sorted(populacao,key = lambda item:(item[len(populacao[0]) - 1]))
    #print("Populacao ordenada: ", populacao_ordenada)

    for i in range(len(populacao_ordenada)):
        for k in range(len(populacao_ordenada[i])):
            if k == len(populacao_ordenada[i]) - 1:
                del(populacao_ordenada[i][k])

    return populacao_ordenada

#Para evitar cair num otimo local, taxa de mutação irá detereminar a probabilidade de um gene sobrer mutação, sugestão variar e 1 a 5%)
# Quando algum gene é escolhido para sofrer mutação determinamos o gene que será mutado através da roleta (com todos os genes com a mesma probabilidade)
def Mutacao(populacao, taxa_mutacao):
    troca = []

    for i in range(len(populacao)):
        if numpy.random.choice(a=[True,False], p = (taxa_mutacao, 1-taxa_mutacao)) == True:
            populacao[i].pop()
            troca = numpy.random.choice(a=populacao[i], size=2, replace = False)
            populacao[i].append(populacao[i][0])
            #print("Individuo ", populacao[i] , "vai sofrer mutacao dos genes: ", troca)
            for k in range(len(populacao[i])):
                if populacao[i][k] == troca[0]:
                    populacao[i][k] = troca[1]
                else :
                    if populacao[i][k] == troca[1]:
                        populacao[i][k] = troca[0]
            #print("novo individuo: ", populacao[i])

    return populacao

def Reprodução(populacao, pares, lista_vertice):
    novapopulacao = []
    individuoA = []
    individuoB = []
    individuogeradoA = []
    individuogeradoB = []
    geneinedito = True
    generepetido = False

    #print(pares)

    for i in range(0, len(pares)-1, 2):
        individuogeradoA = []
        individuogeradoB = []

        #print("PAR REPRODUCAO: ", pares[i], "INDIVIDUO1: ", pares[i][0], "INDIVIDUO2: ", pares[i][1])

        individuoA = populacao[pares[i]]
        individuoB = populacao[pares[i+1]]
        ponto = numpy.random.choice(a=numpy.arange(start=1, stop=len(individuoB)-1))

        #print("Individuo A: ", individuoA, "Individuo B: ", individuoB, "Ponto de break: ", ponto)

        for k in range(len(individuoA)):
            if k == 0:
                origemA = individuoA[k]
                origemB = individuoB[k]
            if(k < ponto):
                individuogeradoA.append(individuoA[k])
                individuogeradoB.append(individuoB[k])
                #print("Adicionando ponto: ", k, "Adicionou o ponto antes do break em A:", individuoA[k], "Adicionou o ponto antes do break em  B:", individuoB[k])
            else:
                if k == len(individuoA) - 1:
                    individuogeradoA.append(origemA)
                    individuogeradoB.append(origemB)
                    #print("Adicionando ponto: ", k, "Adicionou a origem A:", origemA, "Adicionou a origem B:", origemB)
                else:
                    for i in individuogeradoA:
                        if individuoB[k] == i:
                            generepetido = True
                    if generepetido == True:
                        for m in lista_vertice:
                            for n in individuogeradoA:
                                if m == n:
                                    geneinedito = False
                            for j in range(len(individuoB)-1):
                                if j > k and m == individuoB[j]:
                                    geneinedito = False
                            if geneinedito == True:
                                individuogeradoA.append(m)
                                #print("Adicionando ponto: ", k, "Adicionando o ponto com base na lista de vertice em A: ", m)
                                break
                            else:
                                geneinedito = True
                    else:
                        individuogeradoA.append(individuoB[k])
                        #print("Adicionando ponto: ", k, "Adicionando o ponto normalmente em A:", individuoB[k])
                    geneinedito = True
                    generepetido = False    
                    
                    for i in individuogeradoB:
                        if individuoA[k] == i:
                            generepetido = True
                    if generepetido == True:        
                        for m in lista_vertice:
                            for n in individuogeradoB:
                                if m == n:
                                    geneinedito = False
                            for j in range(len(individuoA)-1):
                                if j > k and m == individuoA[j]:
                                    geneinedito = False
                            if geneinedito == True:
                                individuogeradoB.append(m)
                                #print("Adicionando ponto: ", k, "Adicionando o ponto com base na lista de vertice em B: ", m)
                                break
                            else:
                                geneinedito = True
                    else:
                        individuogeradoB.append(individuoA[k])
                        #print("Adicionando ponto: ", k, "Adicionando o ponto normalmente em B:", individuoA[k])
                    geneinedito = True
                    generepetido = False
        
        novapopulacao.append(individuogeradoA)
        novapopulacao.append(individuogeradoB)

    #for i in range(len(novapopulacao)):
    #    print("O individuo ", i+1, " ficou: ", novapopulacao[i])
    
    return novapopulacao

def Selecao(populacao, list_probabilidade, taxa_cruzamento):
    list_pares = []
    
    n_pares = round(taxa_cruzamento*(len(populacao)/2))
    #print("N_PARES", n_pares)
    list_pares = numpy.random.choice(a=len(populacao), size = n_pares*2, replace = False, p=list_probabilidade)
    #print("PARES: ", list_pares)
        
    return list_pares

#RETORNA UM ARRAY COM A PROBABILIDADE DE VISITAR CADA UM DOS VIZINHOS ELEGÍVEL DA "ORIGEM". 
def Probabilidade(grafo, populacao):
    fitness = []
    probabilidade = []
    inversa_distancia = []
    somatorio = 0

    fitness = Fitness(grafo, populacao)

    for i in range(len(fitness)):
        inversa_distancia.append(1 / fitness[i])
    for i in range(len(inversa_distancia)):
        somatorio += inversa_distancia[i]
    for i in range(len(inversa_distancia)):
        probabilidade.append(inversa_distancia[i] / somatorio)

    return probabilidade

def Fitness(grafo, populacao):
    lista_fitness = []

    for i in range(len(populacao)):
        individuo = []
        somatorio_distancia = 0
        individuo = populacao[i]
        #print(individuo)
        for k in range((len(populacao[i]))-1):
            #print("Somando o caminho de ", individuo[k]," --> ", individuo[k+1])
            somatorio_distancia = somatorio_distancia + grafo[individuo[k]][individuo[k+1]]["weight"]
        #print("individuo " , i+1 , ": ", individuo, "Somatorio de distancia", somatorio_distancia)
        
        lista_fitness.append(somatorio_distancia)
    
    return lista_fitness

def geraIndividuo(lista_vertice):
    individuo = []
    vertices_individuo = []
    
    for endereco in lista_vertice:
        vertices_individuo.append(endereco) 

    for k in range(len(lista_vertice)):
        gene = numpy.random.choice(a=vertices_individuo)
        if k == 0:
           origem = gene
        #print("O gene", k , " é: ", gene)
        individuo.append(gene)
        vertices_individuo.remove(gene)

    individuo.append(origem)
    #print("Individuo: ", individuo)
    
    return individuo

def AlgoritmoGenetico(grafo, lista_vertice, tamanho_populacao, taxa_mutacao, taxa_cruzamento, n_iteracoes):
    populacao = []
    fitness = []
    list_probabilidade = []
    pares = []
    proxima_geracao = []
    nova_geracao = []
    nova_populacao = []
    rotaFinal = []

    parada = False
    #melhortempoRodada = []

    for i in range(tamanho_populacao):
        populacao.append(geraIndividuo(lista_vertice))

    # Criterio de parada -> pode ser por tempo de exeução, n de iterações ou qualidade da resposta
    #Acredito que uma boa condição de parada é se passar 2 gerações sem melhorar a menor distancia, o algoritmo é pausado
    

    #PARA ALTERAR O CRITERIO DE PARADA  
    i = 0
    #while (parada == False):
    for i in range(n_iteracoes):

        list_probabilidade = Probabilidade(grafo, populacao)
        pares = Selecao(populacao, list_probabilidade, taxa_cruzamento)
        proxima_geracao = Reprodução(populacao, pares, lista_vertice)
        nova_geracao = Mutacao(proxima_geracao, taxa_mutacao)

        #fitness = Fitness(grafo, populacao)
        #for i in range(len(populacao)):
        #    print('POPULACAO ', i, ' é: ', populacao[i], "a distancia total é: ", fitness[i]) 
        #fitness = Fitness(grafo, nova_geracao)
        #for i in range(len(nova_geracao)):
        #    print("NOVA_POPULACAO ", i, " é: ", nova_geracao[i], "a distancia total é: ", fitness[i]) 

        nova_populacao = populacao + nova_geracao
        
        
        populacao = AtualizaPopulacao(grafo, nova_populacao, tamanho_populacao)
        fitness = Fitness(grafo, populacao)
        
        
        
        #for k in range(len(populacao)):
        #    print("O individuo ", k, " é: ", populacao[k], "a distancia total é: ", fitness[k]) 
        
        #print("Menor tempo da ", i+1, " é: ", fitness[0]) 
        print(fitness[0]) 
        # MECANISMO DE PARADA - 3 rodadas sem emlhorar o menor tempo
        #melhortempoRodada.append(fitness[0])
        #print("Melhor tempo: ", melhortempoRodada)
        #if len(melhortempoRodada) > 2:
        #    if (melhortempoRodada[len(melhortempoRodada) - 1] == melhortempoRodada[len(melhortempoRodada) - 2] ) and (melhortempoRodada[len(melhortempoRodada) - 2] == melhortempoRodada[len(melhortempoRodada) - 3]):
        #        print("Levou ", i+1, " iteracoes")
        #        parada = True
        
        # MECANISMO DE PARADA - estabilização
        #if fitness[0] == fitness[len(fitness) - 1]:
        #    print("Levou ", i+1, " iteracoes")
        #    parada = True
        
        #i = i+1
        #print("Fim da", i, " iteração.")

    rotaFinal.append(fitness[0])
    rotaFinal.append(populacao[0])
    
    #print(rotaFinal)
    
    return rotaFinal