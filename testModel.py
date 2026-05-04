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

source = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
print(f"\n{'=' * 40}\n")
print(f"Le fermate sono: {len(nodiBFS)}")
print("Le prime 10 fermate sono: (BFS)")
# li possiamo raggiungere tutti -> stampiamo i primi 10
for i in range (0, 10):
    print(f"{i+1}. {nodiBFS[i]}")

nodiDFS = model.getDFSNodesFromEdges(source)
print(f"\n{'=' * 40}\n")
print(f"Le fermate sono: {len(nodiDFS)}")
print("Le prime 10 fermate sono: (DFS)")
for i in range (0, 10):
    print(f"{i+1}. {nodiDFS[i]}")

print(f"\n{'=' * 40}\n")
print("Gli archi con peso 2 sono:")
model.buildGraphPesato() # devo prima creare grafo pesato
archiMaggiori = model.getArchiPesoMaggiore()
count = 1
for a in archiMaggiori:
    print(f"{count}. {a[0]} -> {a[1]}: {a[2]["weight"]}")
    count += 1