import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._circuits = []
        self._idMapCircuits = {}


    def creaGrafo(self, datai, dataf):
        self._grafo.clear()
        self._circuits = DAO.getAllCircuits()
        self._idMapCircuits = {a.circuitId: a for a in self._circuits}
        self._grafo.add_nodes_from(self._circuits)

        pesi = DAO.getPesiCircuiti(datai, dataf)
        coppie = DAO.getEdges(datai, dataf)

        for c in coppie:
            idA, idB = c["idA"], c["idB"]
            a = self._idMapCircuits[idA]
            b = self._idMapCircuits[idB]
            peso = pesi.get(idA, 0) + pesi.get(idB, 0)
            self._grafo.add_edge(a, b, weight=peso)


    def getAllYears(self):
        return DAO.getAllYears()

    def getAllCircuits(self):
        return DAO.getAllCircuits()


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getDettagli(self):
        if len(self._grafo.nodes) == 0:
            return None

        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)

        risultato = []
        for nodo in piuGrande:
            archi = self._grafo.edges(nodo, data=True)
            if archi:
                pesoMax = max(dati["weight"] for _, _, dati in archi)
            else:
                pesoMax = 0  # nodo isolato finito da solo nella componente
            risultato.append((nodo, pesoMax))

        risultato.sort(key=lambda x: x[1], reverse=True)
        return risultato
