from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() # inizializzo grafo

        self.idMapFermate = {} # standard
        for f in self._fermate:
            self.idMapFermate[f.id_fermata] = f # creo dizionario: chiave è id, valore è oggetto Fermata

    def buildGraph(self):
        # prima svuoto grafo (magari riempito da esercizi precedenti)
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate) # ogni nodo corrisponde a una fermata
        self.addEdges2()

    # def addEdges(self): # molto molto lento -> non va bene
        # verifiche due nodi (fermate) hanno connessione
        # due cicli for per verificare che ci sia connessione tra fermate
        # for u in self._fermate:
            # for v in self._fermate:
                # if DAO.hasConnesione(u, v): # se ritorna True -> aggiungo nel grafo
                    # self._grafo.add_edge(u, v)

    def addEdges(self): # guardo solo i miei vicini, molto più veloce
        for u in self._fermate:
            # guardo i vicini (nodi con cui è connesso) e li metto negli edge
            for connessione in DAO.getVicini(u):
                v = self.idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges2(self):
        allEdges = DAO.getAllEdges()
        for connessione in allEdges:
            u = self.idMapFermate[connessione.id_stazP]
            v = self.idMapFermate[connessione.id_stazA]
            self._grafo.add_edge(u, v)


    # per accedere a variabile privata
    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate