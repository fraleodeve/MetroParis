from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnesione(u: Fermata, v: Fermata):
        # c'è tabella connessione nel database
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from connessione c 
                    where c.id_stazP = %s and c.id_stazA = %s"""
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        # a noi basta sapere se c'è o non c'è

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0
        # se len è maggiore di 0, return True

    @staticmethod
    def getVicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from connessione c 
                    where c.id_stazP = %s"""
        cursor.execute(query, (u.id_fermata,)) # ricordarsi di mettere la virgola
        # creo dataclass per memorizzare dati che raccolgo

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result




