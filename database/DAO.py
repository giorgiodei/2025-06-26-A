from database.DB_connect import DBConnect
from model.circuits import Circuits


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct year
from seasons s
order by year desc


"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select *
from circuits
"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuits(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllResults(circuitId, datai,dataf):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r.`year`, r2.driverId, r2.`position`  
from  races r, results r2 
where r.raceId =r2.raceId 
and r.circuitId =%s
and r.`date` >= %s and r.`date` <= %s
"""
        cursor.execute(query,(circuitId,datai,dataf,))

        res = []
        for row in cursor:
            res.append(Circuits.addPiazzamento(**row))

        cursor.close()
        cnx.close()
        return res
