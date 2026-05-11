import geopy

from database.DAO import DAO
import networkx as nx
import geopy.distance

from model.fermata import Fermata


def getPesoTempoPercorrenza(partenza: Fermata, arrivo: Fermata, velocita):
    dist = geopy.distance.distance((partenza.coordX, partenza.coordY), (arrivo.coordX, arrivo.coordY)).km
    time = dist/velocita * 60 # in minuti
    return time


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() # inizializzo grafo diretto

        self.idMapFermate = {} # standard
        for f in self._fermate:
            self.idMapFermate[f.id_fermata] = f # creo dizionario: chiave è id, valore è oggetto Fermata
        # per mappare chiave primaria e oggetto
        # utile per recuperare oggetto a partire da id (stringa o intero)

    def buildGraph(self): # riempio grafo
        # prima svuoto grafo (magari riempito da esercizi precedenti)
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate) # ogni nodo corrisponde a una fermata
        # metto come valore una lista di oggetti
        self.addEdges2()
        # numero archi viene diverso: 1428 vs 1476 (previste)
        # questo perchè posso avere fermate collegate tra di loro con più linee
        # alcuni archi sono ripetuti
        # quindi inizializzo un MultiGraph o un grafo pesato

    def buildGraphPesato(self):
        # rimane anche un diGraph
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)  # uguale a prima
        # self.addEdgesPesati()
        self.addEdgesPesatiTempi()

    # def addEdges(self): # molto molto lento (perchè faccio doppio ciclo, aggiungo un arco alla volta) -> impiega 109s
        # posso quando il grafo è piccolo

        # verifiche due nodi (fermate) hanno connessione
        # due cicli for per verificare che ci sia connessione tra fermate
        # for u in self._fermate:
            # for v in self._fermate:
                # if DAO.hasConnesione(u, v): # se ritorna True -> aggiungo nel grafo
                    # self._grafo.add_edge(u, v)

    def addEdges(self): # guardo solo i miei vicini, molto più veloce -> impiega meno di 1s
        for u in self._fermate:
            # guardo i vicini (nodi con cui è connesso) e li metto negli edge
            for connessione in DAO.getVicini(u):
                v = self.idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)


    def addEdges2(self): # faccio una sola query semplice -> impiega meno di 1s
        allEdges = DAO.getAllEdges()
        for connessione in allEdges:
            u = self.idMapFermate[connessione.id_stazP]
            v = self.idMapFermate[connessione.id_stazA]
            self._grafo.add_edge(u, v)

    def addEdgesPesati(self):
        # riutilizzo principio funzionamento metodo addEdges2
        # ma conto quante volto provo ad aggiungere arco
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdges()
        for connessione in allEdges:
            u = self.idMapFermate[connessione.id_stazP]
            v = self.idMapFermate[connessione.id_stazA]

            if self._grafo.has_edge(u, v): # grafo come un dizionario
                self._grafo[u][v]['weight'] += 1 # incremento peso
            else: # se arco ancora non esiste
                self._grafo.add_edge(u, v, weight = 1)

    # in alternativa delego al DAO
    # dipende da quanto è difficile scrivere query SQL (qua facile)
    def addEdgesPesati2(self):
        # delega calcolo del peso alla query sql
        # semplifico codice python
        self._grafo.clear_edges()
        allEdgesPesati = DAO.getAllEdgesPesati()
        # tupla (id_stazP, id_stazA, peso)

        for e in allEdgesPesati:
            u = self.idMapFermate[e[0]]
            v = self.idMapFermate[e[1]]
            peso = e[2]

            self._grafo.add_edge(u, v, weight = peso)

    # 4 metodi uguali per esplorare il grafico (cambia come viene restituito il grafico)
    def getBFSNodesFromEdges(self, source):
        # esploro per livelli
        archi = nx.bfs_edges(self._grafo, source) # iterable di tuple
        nodiBFS = []
        for u, v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source) # iterable di tuple
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS # stessi elementi a prima, ma diverso ordine degli elementi

    # uso albero di visita
    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges)
        nodi = list(tree.nodes) # contiene anche source
        return nodi

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges)
        nodi = list(tree.nodes)  # contiene anche source
        return nodi

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)
        # mettendo data = True, inserisco anche gli attributi associati (il peso)

        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1: # metodo che mi restituisce i pesi
                # analogo a fare: self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori

    def addEdgesPesatiTempi(self):
        # creo archi in cui peso è pari al tempo di percorrenza di quell'arco ottenuto come rapporto tra distanza fra
        # le stazioni e la velocità di percorrenza

        self._grafo.clear_edges()
        allEdgesVel = DAO.getAllEdgesVel()
        for e in allEdgesVel:
            u = self.idMapFermate[e[0]]
            v = self.idMapFermate[e[1]]
            peso = getPesoTempoPercorrenza(u, v, e[2])
            self._grafo.add_edge(u, v, weight = peso)

    def getShortestPath(self, partenza, arrivo):
        return nx.single_source_dijkstra(self._grafo, partenza, arrivo)


    # per accedere a variabile privata
    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate