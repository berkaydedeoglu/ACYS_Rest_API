from flask_restful import Resource

class Makineler (Resource):
    def __init__(self, database):
        Resource()
        self._cursor = database.cursor()
    
    def get(self):
        sorgu  = """SELECT M.MakineAdi, O.OkuyucuID, O.AntenID FROM Makineler AS M 
                    JOIN MakineOkuyuculari AS  O ON O.MakineID = M.MakineID"""

        db_cevap = self._cursor.execute(sorgu)

        return self.cevap_olustur(db_cevap)

    
    def cevap_olustur(self, db_cevap: tuple)-> dict:
        exdi = {"ad": "", "okuyucu": "", "anten": ""}

        return [{"ad": i[0], "okuyucu": i[1], "anten": i[2]} for i in db_cevap]

