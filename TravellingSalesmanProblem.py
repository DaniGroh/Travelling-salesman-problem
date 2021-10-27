#TRABALHO FINAL DE GRADUACAO - OTIMIZAÇÃO DE ROTAS
#
#ALUNO: DANIEL ARRUDA GROH	- 31061
#PROFESSOR ORIENTEDOR: GIOVANNI BERNARDES; 
#PROFESSOR CO-ORIENTEDOR: WILLIAN;
#
#09/10/2020

import googlemaps
import json
import os.path
import time

import AntColonyOptimization as AntColonyOptimization
import GeneticAlgorithm as GeneticAlgorithm

import networkx as nx

def ConsultaGmaps(origem, destino):
        #Geocoding an address
        #geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
        #Look up an address with reverse geocoding
        #reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
        directions_result = gmaps.distance_matrix(origem,destino)
        #directions_result = gmaps.directions(origem,destino)
        if directions_result["status"] == "OK":
            #Desta variavel consulta vem uma string. Essa string contem a informação do tempo para se locomover do local "origem" até o local "destino"
            return directions_result["rows"][0]["elements"][0]["distance"]['value']

def CarregaFuncionarios():
    listaFuncionarios = []
    if os.path.exists('base/15enderecos.json'): 
        with open('base/15enderecos.json','r') as json_file:
            listaFuncionarios = json.load(json_file)
    return listaFuncionarios

def CarregaDistancias():
    listaDistancias = []
    if os.path.exists('base/15.json'): 
        with open('base/15.json','r') as json_file:
            listaDistancias = json.load(json_file)
    return listaDistancias

def SalvaFuncionarios(listaFuncionarios):
    with open('base/15enderecos.json', 'w') as json_file:
        json.dump(listaFuncionarios, json_file, indent=4)

def SalvaDistancias(listaDistancias):
    with open('base/15.json', 'w') as json_file:
        json.dump(listaDistancias, json_file, indent=4)

def DesenhaGrafo(listaEnderecos, listaDistancias):
    grafo = nx.Graph()
    n = 0
    for endereco in listaEnderecos:
        grafo.add_node(endereco, visitado = False)
    for i in range(len(listaEnderecos)):
        for j in range((i+1),len(listaEnderecos)):
            if listaEnderecos[i] != listaEnderecos[j]:
                grafo.add_edge(listaEnderecos[i], listaEnderecos[j])
                grafo[listaEnderecos[i]][listaEnderecos[j]]["weight"] = listaDistancias[n]
                grafo[listaEnderecos[i]][listaEnderecos[j]]["feromonio"]= 100
                n = n+1
    return grafo

def main():
    grafo = nx.Graph()
    listaEnderecos = []
    listaDistancias = []

    rotaFinalCF = []
    rotaCF = []
    rotaFinalGA = []
    rotaGA = []
    origem = "1"

    listaFuncionarios = CarregaFuncionarios()
    listaDistancias = CarregaDistancias()
    
    for pessoa in listaFuncionarios:
        listaEnderecos.append(pessoa["endereco"])    

    #for i in range(len(listaEnderecos)):
    #    for j in range((i+1),len(listaEnderecos)):
    #        if listaEnderecos[i] != listaEnderecos[j]:
    #            listaDistancias.append(ConsultaGmaps(listaEnderecos[i], listaEnderecos[j]))

    
    grafo = DesenhaGrafo(listaEnderecos, listaDistancias)
    ordenaRota = len(listaEnderecos)

    #for i in range(len(listaEnderecos)):
    #    for j in range(len(listaEnderecos)):
    #        if listaEnderecos[i] != listaEnderecos[j]:
    #            print("Verifica o vertice: ", listaEnderecos[i], "- ", listaEnderecos[j], "Peso: ", grafo[listaEnderecos[i]][listaEnderecos[j]]["weight"], "Feromonio: ", grafo[listaEnderecos[i]][listaEnderecos[j]]["feromonio"])

    coef_evaporacao = 0.5
    atualizacao_feromonio = 0.03
    n_iteracoes = 200

    inicio_colonia = time.time()
    rotaCF = AntColonyOptimization.SistemaColoniaFormiga(grafo, origem, listaEnderecos, coef_evaporacao, atualizacao_feromonio, n_iteracoes)
    fim_colonia = time.time()
    tempo_colonia = fim_colonia - inicio_colonia
    #print(rotaCF)

    for destino in range(len(rotaCF[1])):
        if rotaCF[1][destino] == origem :
            ordenaRota = destino
            rotaFinalCF.append(rotaCF[1][destino])
        if destino > ordenaRota :
            rotaFinalCF.append(rotaCF[1][destino])
    
    if ordenaRota != (len(rotaCF[1])-1) :
        for destino in range(len(rotaCF[1])):
            if destino > 0 and destino <= ordenaRota:
                rotaFinalCF.append(rotaCF[1][destino])

    print("A melhor distancia encontrada pelo agoritmo de colonia de formiga: ", rotaCF[0], ". E a rota: ", rotaFinalCF, " O tempo de execução foi de: ", tempo_colonia)
    
    tamanho_populacao = 75
    taxa_mutacao = 0.5
    ordenaRota = len(listaEnderecos)
    taxa_cruzamento = 0.7
    n_iteracoes = 500

    inicio_GA = time.time()
    rotaGA = GeneticAlgorithm.AlgoritmoGenetico(grafo, listaEnderecos, tamanho_populacao, taxa_mutacao, taxa_cruzamento, n_iteracoes)
    fim_GA = time.time()
    tempo_GA = fim_GA - inicio_GA
    #print(rotaGA)

    for destino in range(len(rotaGA[1])):
        if rotaGA[1][destino] == origem :
            ordenaRota = destino
            rotaFinalGA.append(rotaGA[1][destino])
        if destino > ordenaRota :
            rotaFinalGA.append(rotaGA[1][destino])
    
    if ordenaRota != (len(rotaGA[1])-1) :
        for destino in range(len(rotaGA[1])):
            if destino > 0 and destino <= ordenaRota:
                rotaFinalGA.append(rotaGA[1][destino])

    print("A melhor distancia encontrada pelo agoritmo genetico: ", rotaGA[0], ". E a rota: ", rotaFinalGA, " O tempo de execução foi de: ", tempo_GA)

    #SalvaDistancias(listaDistancias)
    #SalvaFuncionarios(listaFuncionarios)
    
main()