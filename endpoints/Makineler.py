from flask_restful import Resource

class Makineler (Resource):
    def __init__(self, database):
        Resource()
        self._cursor = database.cursor()
    
    def get(self):
        sorgu  = """SELECT M.MakineID, M.MakineAdi, M.AntenID, O.OkuyucuID
                    From Makineler as M LEFT JOIN Antenler as O on (O.AntenNo = M.AntenID)"""

        db_cevap = self._cursor.execute(sorgu)

        return self.cevap_olustur(db_cevap)

    
    def cevap_olustur(self, db_cevap: tuple)-> dict:
        
        makineler = [{"id": i[0], "ad":i[1], "anten": i[2], "okuyucu": i[3]} for i in db_cevap]
        return {"makineler": makineler} 


