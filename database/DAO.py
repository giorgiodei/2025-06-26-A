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
    def getEdges(datai, dataf):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct c1.circuitId as idA, c2.circuitid as idB
from
(select r1.circuitId, r1.`year`       
from  races r1, results r2, circuits c 
where r1.circuitId =c.circuitId 
and r1.raceId = r2.raceId and
r2.positionOrder is not null
and r1.`year` between %s and %s
) c1,
(
select r1.circuitId, r1.`year`       
from  races r1, results r2, circuits c 
where r1.circuitId =c.circuitId 
and r1.raceId = r2.raceId and
r2.positionOrder is not null
and r1.`year` between %s and %s
)  c2
where
c1.circuitid <c2.circuitid

"""
        cursor.execute(query,(datai,dataf,datai,dataf,))

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getPesiCircuiti(datai, dataf):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            select r1.circuitId, count(*) as peso
            from races r1, results r2
            where r1.raceId = r2.raceId
              and r2.position is not null
              and r1.`year` between %s and %s
            group by r1.circuitId
        """
        cursor.execute(query, (datai, dataf))
        res = {row["circuitId"]: row["peso"] for row in cursor}
        cursor.close()
        cnx.close()
        return res