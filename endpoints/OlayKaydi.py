from flask_restful import Resource, reqparse
from flask import Request


class OlayKaydi(Resource):
    """Veritabanında olay kayıtlarını uygun filtrelerle gönderen sınıf.
    filtreler ve dönüş değerleri için bkz. ./templates/Hosgeldin.html"""

    def __init__(self, database):
        """
        Parametreler:
            -> database: Kayıtların bulunduğu veritabanının referansı
        """
        super()

        # Veritabanında işlem yapabilmek için oluşturulan imleç nesnesi.
        self._cursor = database.cursor()

        # Gelen parametrelei izleyip ayrılmasını sağlayan nesne
        self._parser = reqparse.RequestParser()

    def get(self, yil=None, ay=None, gun=None):
        """Bu endpointin get sorgusunu karşılayan metod. Detaylı bilgi
        için bkz. ./templates/Hoşgeldin.html

        Parametreler:
            -> yil: İstenilen yıla göre filtrenlenme
            -> ay : İstenilen aya göre filtrelenme
            -> gun: istenilen fikre göre filtrelenme.

        NOT: Yıl verilmeden ay ve gün, ay verilmeden gün filtresi çalışmaz.
        """

        # Sorguyla verilen argümanların okunması.
        self._parser.add_argument("kayit_sayisi")
        self._parser.add_argument("makine_adi")

        sorgu = self._sorgu_olustur(yil, ay, gun)
        print(sorgu)
        db_cevap = self._cursor.execute(sorgu)

        return self._cevap_olustur(db_cevap)

    def post(self):
        """Bu endpointin post sorgusunu karşılayan metod. Detaylı bilgi
        için bkz. ./templates/Hoşgeldin.html
        """

        def kayit_olustur():
            # Gelen parametrelerin okunması için kaydının yapılması.
            self._parser.add_argument("makine")
            self._parser.add_argument("zaman")
            self._parser.add_argument("mesaj")

            # Gelen parametrelerin ayrıştırılması.
            args = self._parser.parse_args()

            kayit = "INSERT INTO Olaylar VALUES ('{}', '{}', convert(datetime, '{}'))".format(
                args["makine"], args["mesaj"], args["zaman"])

            return kayit

        kayit = kayit_olustur()
        self._cursor.execute(kayit)
        self._database.commit()

        return (), 200

    def _sorgu_olustur(self, yil=None, ay=None, gun=None):

        args = self._parser.parse_args()

        sorgu = "SELECT {} FROM Olaylar WHERE 1=1 "

        if args["kayit_sayisi"]:
            sorgu = sorgu.format(args["kayit_sayisi"])
        else:
            sorgu = sorgu.format("*")

        if args["makine_adi"]:
            sorgu += "AND MachineName = args[{}]".format(args["makine_adi"])

        # TODO: Çok fazla iç içe if tanımlandı.
        if yil:
            sorgu += "AND DATEPART(YEAR, Times) = {} ".format(yil)

            if ay:
                sorgu += "AND DATEPART(MONTH, Times) = {} ".format(ay)

                if gun:
                    sorgu += "AND DATEPART(DAY, Times) = {} ".format(gun)

        return sorgu

    def _cevap_olustur(self, db_cevap):
        """Veritabanından gelen cevabı json formatına dönüştürebilecek hale dönüştürür. """
        
        return {"olaylar": [{
            "makine": i[2], "olay": i[1], "zaman": str(i[3])
        }for i in db_cevap]}
