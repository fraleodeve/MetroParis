from database.DAO import DAO
import networkx as nx

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




    # per accedere a variabile privata
    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate