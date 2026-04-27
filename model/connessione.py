from dataclasses import dataclass

@dataclass
class Connessione: # copio da database
    id_connessione: int
    id_linea: int
    id_stazP: int
    id_stazA: int


    def __hash__(self):
        return hash(self.id_connessione)

    def __str__(self):
        return f"{self.id_connessione}"

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione