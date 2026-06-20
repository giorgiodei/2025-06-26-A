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


    def getAllYears(self):
        return DAO.getAllYears()

    def getAllCircuits(self):
        return DAO.getAllCircuits()


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)