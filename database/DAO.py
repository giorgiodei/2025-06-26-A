from database.DB_connect import DBConnect
from model.circuits import Circuits


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM circuits"
        cursor.execute(query)

        res = []
        for row in cursor:
            c = Circuits(
                circuitId=row['circuitId'],
                circuitRef=row['circuitRef'],
                name=row['name'],
                location=row['location'],
                country=row['country'],
                lat=row['lat'],
                lng=row['lng'],
                alt=row['alt'],
                url=row['url']
            )
            res.append(c)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct year
                       from seasons s
                       order by year desc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getAllResults(circuitId, datai,dataf):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        select r.`year`, r2.driverId, r2.`position`  
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

    @staticmethod
    def getPesoArco(circuitId1, circuitId2, datai, dataf):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT 
    c1.peso_c1 + c2.peso_c2 AS peso_totale_arco,
    c1.numero_gare_c1,
    c2.numero_gare_c2
FROM 
    (SELECT 
        COUNT(DISTINCT r.raceId) AS numero_gare_c1,
        COUNT(r2.driverId) AS peso_c1
     FROM races r, results r2
     WHERE r.raceId = r2.raceId
       AND r.circuitId = %s
       AND r.year BETWEEN %s AND %s
       AND r2.position IS NOT NULL 
       AND r2.position > 0
    ) AS c1,

    (SELECT 
        COUNT(DISTINCT r.raceId) AS numero_gare_c2,
        COUNT(r2.driverId) AS peso_c2
     FROM races r, results r2
     WHERE r.raceId = r2.raceId
       AND r.circuitId = %s
       AND r.year BETWEEN %s AND %s
       AND r2.position IS NOT NULL 
       AND r2.position > 0
    ) AS c2
"""
        cursor.execute(query,(circuitId1,datai,dataf,circuitId2,datai,dataf,))

        """res = []
        for row in cursor:
            res.append(row)"""

        arco=cursor.fetchone()

        cursor.close()
        cnx.close()
        return arco