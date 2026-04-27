# per fare prove sul grafo
from model.model import Model

model = Model()
print("Numero nodi:", model.get_numNodi()) # 0
print("Numero archi:", model.get_numArchi()) # 0
model.buildGraph()

# stampare numero di nodi
print("Numero nodi:", model.get_numNodi()) # 619
print("Numero archi:", model.get_numArchi()) # 1428