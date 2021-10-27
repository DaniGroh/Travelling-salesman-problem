import networkx as nx
import numpy

#RETORNA UM ARRAY CONTENDO 1/PESO DE CADA ARESTA QUE CONECTA O NÓ "ORIGEM"
def InversaDistancia(grafo, origem):
    inversa_distancia = {}
    list_vizinhos = list(grafo.neighbors(origem))
    
    #REMOVENDO VIZINHOS QUE JA FORAM VISITADOS
    for i in list(grafo.neighbors(origem)):
        if grafo.nodes[i]["visitado"] == True:
            list_vizinhos.remove(i)
    
    for i in range(len(list_vizinhos)):
        inversa_distancia[(origem, list_vizinhos[i])] = 1 / grafo[origem][list_vizinhos[i]]["weight"]

    return inversa_distancia

#Txy -> INVERSA DA DISTANCIA , Nxy -> FEROMONIO DA ARESTA
#RETORNA UM ARRAY COM A PROBABILIDADE DE VISITAR CADA UM DOS VIZINHOS ELEGÍVEL DA "ORIGEM". 
#ELE CALCULA A PROBABILIDADE DA SEGUINTE MANEIRA "(Txy * Nxy)/ SOMATORIA(Txy * Nxy)
def ProbabilidaAresta(grafo, origem):
    probabilidade_aresta = {}
    inversa_distancia = InversaDistancia(grafo, origem)
    list_vizinhos = list(grafo.neighbors(origem))

    #REMOVENDO VIZINHOS QUE JA FORAM VISITADOS
    for i in list(grafo.neighbors(origem)):
        if grafo.nodes[i]["visitado"] == True:
            #print("Removendo: ", i)
            list_vizinhos.remove(i)

    somatorio_TxyNxy = 0
    for i in range(len(list_vizinhos)):
        somatorio_TxyNxy += inversa_distancia[(origem, list_vizinhos[i])] * grafo[origem][list_vizinhos[i]]["feromonio"]
        #print("Trajeto: ",origem , "-", ": ", list_vizinhos[i], "Feromonio da aresta: ", grafo[origem][list_vizinhos[i]]["feromonio"])
    
    for i in range(len(list_vizinhos)):
        probabilidade_aresta[(origem, list_vizinhos[i])] = (inversa_distancia[(origem, list_vizinhos[i])] * grafo[origem][list_vizinhos[i]]["feromonio"] / somatorio_TxyNxy)
    #print("Probabilidade de cada: ", probabilidade_aresta)
    return probabilidade_aresta

# DEFINIR PROXIMO DESTINO COM BASE NA PROBABILIDADE DE CADA ARESTA
def ProximoVertice(grafo, origem):
    dict_probabilidade_aresta = ProbabilidaAresta(grafo, origem)

    vizinhos_origem = list(grafo.neighbors(origem))
    
    #REMOVENDO VIZINHOS QUE JA FORAM VISITADOS
    for i in list(grafo.neighbors(origem)):
        if grafo.nodes[i]["visitado"] == True:
            vizinhos_origem.remove(i)

    list_probabilidade = []
    
    for j in range(len(vizinhos_origem)):
        list_probabilidade.append(dict_probabilidade_aresta[(origem, vizinhos_origem[j])])
    #print("Checar Probabilidade: ", list_probabilidade)
    #print("Checar Vizinhos: ", vizinhos_origem)
    
    #FORMIGAS ESCOLHEM SEU PROCIMO VERTICE DE ACORDO COM A REGRA DA ROLETA, CONSIDERANDO AS PROBABILIDADES DE CADA VIZINHO ELEGIVEL
    checar_destino = []
    checar_destino.append(numpy.random.choice(a=vizinhos_origem, p=list_probabilidade))
    #print("Destino Escolhido: ", checar_destino[0])

    #FORMIGAS ESCOLHEM SEMPRE O VERTICE COM A MAIOR PROBABILIDADE
    #pos = list_probabilidade.index(max(list_probabilidade, key=float))
    #destino = vizinhos_origem[pos]
    #print("Destino Escolhido: ", destino)

    return checar_destino[0]

# DEFINIR O CAMINHO PERCORRIDO PELA FORMIGA
def Caminho(grafo, posicao_atual, destino, lista_caminho, visitou_todos):
    lista_caminho.append(posicao_atual)
    #print("Posicao atual: ", posicao_atual)
    grafo.nodes[posicao_atual]["visitado"] = True
    flag_visitou_todos = False

    #Coloca a variavel iguala True caso ja tenha visitado todos os nós
    for i in list(grafo.neighbors(posicao_atual)): 
        if grafo.nodes[i]["visitado"] == False:
            flag_visitou_todos = True  
    if flag_visitou_todos == False:
        visitou_todos = True

    if visitou_todos == False:
        proximo_vertice = ProximoVertice(grafo, posicao_atual)
        #print("Nó vistado: ", proximo_vertice)
        Caminho(grafo, proximo_vertice, destino, lista_caminho, visitou_todos)
    elif posicao_atual != destino:
        #print("Voltando pro destino")
        proximo_vertice = destino
        Caminho(grafo, proximo_vertice, destino, lista_caminho, visitou_todos)
    else: 
        #print("Visitou todos")
        for i in list(grafo.nodes):    
            grafo.nodes[i]["visitado"] = False

# ATUALIZA O FEROMÔNIO APÓS A EVAPORAÇÃO
def AtualizarTaxaEvaporacao(grafo, lista_vertice, coeficiente_evaporacao):

    lista_visitado = []
    for k in range(len(lista_vertice)):
        list_vizinhos = list(grafo.neighbors(lista_vertice[k]))
        for i in range(len(list_vizinhos)):
            if list_vizinhos[i] not in lista_visitado:
                tx_evaporacao = (1 - coeficiente_evaporacao) * grafo[lista_vertice[k]][list_vizinhos[i]]["feromonio"]
                grafo[lista_vertice[k]][list_vizinhos[i]]["feromonio"] = tx_evaporacao
                #grafo[list_vizinhos[i]][lista_vertice[k]]["feromonio"] = tx_evaporacao #grafo não é bidirecional
                #print("Trajeto: ", lista_vertice[k], "-", list_vizinhos[i], "Apos evaporacao: ", tx_evaporacao)
        lista_visitado.append(lista_vertice[k])

# ATUALIZA O FEROMÔNIO DEIXADO PELA FORMIGA NA ROTA
def AtualizaTaxaFeromonio(grafo, lista_caminho, lista_vertice, taxa_atualizacao):
    #CALCULA A DISTANCIA TOTAL PERCORRIDA POR CADA FORMIGA
    distanciaTotal = []
    for i in range(len(lista_caminho)):
        caminhoFormiga = lista_caminho[i]
        somatorio = 0
        for j in range(len(caminhoFormiga)-1):
            somatorio += grafo[caminhoFormiga[j]][caminhoFormiga[j+1]]["weight"]
        #print("Trajeto: ", lista_caminho[i] ," Distancia total: ",  somatorio)
        distanciaTotal.append(somatorio)
   
    # ATUALIZA O FEROMÔNIO NA ROTA DEIXADO POR CADA FORMIGA
    for i in range(len(lista_caminho)):
        caminhoFormiga = lista_caminho[i]
        for j in range(len(caminhoFormiga) - 1):
            somatorio = (taxa_atualizacao / distanciaTotal[i]) + grafo[caminhoFormiga[j]][caminhoFormiga[j + 1]]["feromonio"]
            #print("trajeto: ", caminhoFormiga[j], "-", caminhoFormiga[j + 1], "  Feromonio anterior: ", grafo[caminhoFormiga[j]][caminhoFormiga[j + 1]]["feromonio"], "Feromonio depositado", (taxa_atualizacao / distanciaTotal[i]))
            grafo[caminhoFormiga[j]][caminhoFormiga[j + 1]]["feromonio"] =  somatorio
            #grafo[caminhoFormiga[j + 1]][caminhoFormiga[j]]["feromonio"] =  somatorio #valido para grafo não bidirecional
            
    
    #PRINT PARA VERIFICAR A ATUALIZAÇÃO DE FEROMONIO DOS VERTICES
    #for i in range(len(lista_vertice)):
    #    for j in range(len(lista_vertice)):
    #        if lista_vertice[i] != lista_vertice[j]:
    #            print("Verifica o vertice: ", lista_vertice[i], "- ", lista_vertice[j], "Feromonio: ", grafo[lista_vertice[i]][lista_vertice[j]]["feromonio"])

    return distanciaTotal

def SistemaColoniaFormiga(grafo, origem, lista_vertice, coeficiente_evaporacao, atualizacao_feromonio, n_iteracoes):

    lista_caminho_formiga = []
    rotaFinal = []

    melhortempoRodada = []
    parada = False

    n_formigas = 10

    #PARA ALTERAR O CRITERIO DE PARADA
    i = 0
    #while (parada == False):
    for i in range(n_iteracoes):
        distanciaTotal = []
        lista_caminho_formiga = []
        for j in range(n_formigas):
            list_caminho = []
            origem = numpy.random.choice(a=lista_vertice);
            destino = origem
            Caminho(grafo, origem, destino, list_caminho, False)
            lista_caminho_formiga.append(list_caminho)
            #print("Formiga numero :", j+1 , "Caminho percorrido: ", list_caminho, "Distancia percorrida: ", distanciaTotal)
        #print("Atualizando feromonio.")
        AtualizarTaxaEvaporacao(grafo, lista_vertice,coeficiente_evaporacao)
        distanciaTotal = AtualizaTaxaFeromonio(grafo, lista_caminho_formiga, lista_vertice, atualizacao_feromonio)
        
        #for j in range(n_formigas):
        #    print("Formiga numero :", j+1 , "Caminho percorrido: ", lista_caminho_formiga[j], "Distancia percorrida: ", distanciaTotal[j])
        
        i = i+1
        #print("Lista do caminho das formigas: ", distanciaTotal)
        
        melhortempo = distanciaTotal[0]
        for k in range(len(distanciaTotal)):
            if distanciaTotal[k] < melhortempo:
                melhortempo = distanciaTotal[k]

        melhortempoRodada.append(melhortempo)
        #print("Melhor tempo da ", i , " rodada: ", melhortempoRodada[i-1])
        print(melhortempoRodada[i-1])
        
        
        # MECANISMO DE PARADA - não houve avanço no melhor tempo pro 3 iterações
        #if len(melhortempoRodada) > 2:
        #    if (melhortempoRodada[len(melhortempoRodada) - 1] == melhortempoRodada[len(melhortempoRodada) - 2] ) and (melhortempoRodada[len(melhortempoRodada) - 2] == melhortempoRodada[len(melhortempoRodada) - 3]):
        #        print("Levou ", i+1, " iteracoes")
        #        parada = True
        
        # MECANISMO DE PARADA - estabilização
        #melhortempo = distanciaTotal[0]
        #for k in range(len(distanciaTotal)):
        #    if melhortempo != distanciaTotal[k]:
        #        break
        #    else:
        #        if k == len(distanciaTotal) -1:
        #            print("Levou ", i+1, " iteracoes")
        #            parada = True
        
        #print("Fim da ", i, " iteracao")
    
    distanciaFinal = distanciaTotal[0]
    rotaFinal.append([distanciaFinal, lista_caminho_formiga[0]])
    for k in range(len(distanciaTotal)):
        #print("Formiga: ", k, "; Distancia percorrida: " , distanciaTotal[k],  "; Caminho realizado: ",  lista_caminho_formiga[k])           
        if distanciaFinal > distanciaTotal[k]:
            distanciaFinal = distanciaTotal[k]
            rotaFinal.append([distanciaFinal, lista_caminho_formiga[k]])
    #print("Rota final: ", rotaFinal[len(rotaFinal)-1])
    
    return rotaFinal[len(rotaFinal)-1]