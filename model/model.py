import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._circuits = []
        self._idMapActors = {}


    def creaGrafo(self, datai, dataf):

        self._grafo.clear()
        self._circuits = DAO.getAllCircuits()
        self._idMapActors = {a.circuitId: a for a in self._circuits}
        self._grafo.add_nodes_from(self._circuits)

        for c1 in self._circuits:
            for c2 in self._circuits:
                if c1.circuitId < c2.circuitId:
                    arco=DAO.getPesoArco(c1.circuitId, c2.circuitId, datai, dataf)
                    if arco is not None:
                        if arco['numero_gare_c1']>0 and arco['numero_gare_c2']>0:
                            self._grafo.add_edge(c1, c2, weight=arco["peso_totale_arco"])




    def getAllYears(self):
        return DAO.getAllYears()

    def getAllCircuits(self):
        return DAO.getAllCircuits()


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

