from flask_restful import Resource, reqparse
from flask import Request

class OlayKaydi(Resource):
    def __init__(self, cursor):
        super()
        self.cursor = cursor

        self.parser = reqparse.RequestParser()
        
        

    def get(self, yil=None, ay=None, gun=None):
        self.parser.add_argument("kayit_sayisi")
        self.parser.add_argument("makine_adi")

        sorgu = self._sorgu_olustur(yil, ay, gun)
        db_cevap = self.cursor.execute(sorgu)

        return self._cevap_olustur(db_cevap)
    
    def post(self):
        return self._kayit_olustur()





    def _sorgu_olustur(self, yil=None, ay=None, gun=None):
        args = self.parser.parse_args()
        sorgu = "SELECT {} FROM Olaylar WHERE 1=1 "
        if args["kayit_sayisi"]:
            sorgu = sorgu.format(args["kayit_sayisi"])
        else:
            sorgu = sorgu.format("*")
        
        if args["makine_adi"]:
            sorgu += "AND MachineName = args[{}]".format(args["makine_adi"])

        # TODO: Çok fazla iç içe if tanımlanmış.
        if yil:
            sorgu += "AND DATEPART(YEAR, Times) = {} ".format(yil)

            if ay:
                sorgu += "AND DATEPART(MONTH, Times) = {} ".format(ay)

                if gun:
                    sorgu += "AND DATEPART(DAY, Times) = {} ".format(gun)
        
        return sorgu
    
    def _kayit_olustur(self):
        self.parser.add_argument("makine")
        self.parser.add_argument("zaman")
        self.parser.add_argument("mesaj")

        args = self.parser.parse_args()

        kayit = "INSERT INTO Olaylar ({}, {}, {})"
        kayit.format(args["makine"], args["mesaj"], args["zaman"])

        return kayit

    def _cevap_olustur(self, db_cevap):
        
        olaylar = []

        for i in db_cevap:
            sorgu = {"makine": i[1],
                     "olay" : i[2],
                     "zaman": str(i[3])}
            olaylar.append(sorgu)

        return {"olaylar": olaylar}
    