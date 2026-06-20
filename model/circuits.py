import dataclasses
from typing import Dict, List, Tuple


@dataclasses.dataclass
class Circuits():

    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat:float
    lng:float
    alt: int
    url: str
    piazzamenti: Dict[int, List[Tuple[int, int]]] = dataclasses.field(default_factory=dict)
    #ottengo un dizionario avente come chiave un anno e come valore una lista di tuple (driverid, position)


    def __hash__(self):
        return hash(self.circuitId)

    def __eq__(self, other):
        return self.circuitId == other.circuitId

    def __str__(self):
        return self.name

    def addPiazzamento(self, anno, driverId, position):
        if anno not in self.piazzamenti:
            self.piazzamenti[anno] = []
        self.piazzamenti[anno].append((driverId, position))





