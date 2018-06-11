from flask_restful import Resource

class Etiketler(Resource):
    
    def __init__(self, cursor):
        super()
        self._db_cursor = cursor

    def get(self, etiket_tipi=None):
        if etiket_tipi:
            sorgu = "SELECT * FROM Etiketler WHERE EtiketTip={}"
            sorgu = sorgu.format(makine_tipi)
        else:
            sorgu = "SELECT * FROM Etiketler"
        
        etiketler = self._db_cursor.execute(sorgu)

        return self.cevap_olustur(etiketler)

    def post(self):
        pass

    def cevap_olustur(self, cevap):

        etiketler = []

        for i in cevap:
            etiket = {"rfid": i[1], "isim": i[2], "tip": i[3]}
            etiketler.append(etiket)

        cevap = {"etiketler" : etiketler}
        return cevap      