# per fare prove sul grafo
from model.fermata import Fermata
from model.model import Model

model = Model()
print("Numero nodi:", model.get_numNodi()) # 0
print("Numero archi:", model.get_numArchi()) # 0
model.buildGraph()

# stampare numero di nodi
print("Numero nodi:", model.get_numNodi()) # 619
print("Numero archi:", model.get_numArchi()) # 1428
# (meno del numero di connessioni nel database -> perchè a volte si sovrappongono linee)

print()

source = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
print(len(nodiBFS))
# li possiamo raggiungere tutti -> stampiamo i primi 10
for i in range (0, 10):
    print(nodiBFS[i])

print()

nodiDFS = model.getDFSNodesFromEdges(source)
print(len(nodiDFS))
for i in range (0, 10):
    print(nodiDFS[i])