from flask_restful import Resource


class Etiketler(Resource):
    """Veritabanda RFID etiketi taşıyan ve kaydı yapılmış bütün kayıtlara
    erişen ve gereken filtrelerle APIye hizmet eden sınıf.

    Kullanılabilecek metodlar için bkz. ./templates/Hoşgeldin.html"""

    def __init__(self, database):
        """Parametreler:
            -> database: Etiketlerin kayıtlarının bulunduğu veritabanının referansı
        """

        super()

        # Veritabanında işlem yapabilmek için oluşturulan imleç nesnesi.
        self._db_cursor = database.cursor()

    def get(self, etiket_tipi=None):
        """Bu endpointin get sorgusunu karşılayan metod. Detaylı bilgi
        için bkz. ./templates/Hoşgeldin.html

        Parametreler:
            -> etiket_tipi: Sorgunun etiket tipine göre yapılmasını sağlar.
            varsayılan olarak None'dur. Bu da tüm verilerin sorgulanmasını 
            sağlar. 
        """

        if etiket_tipi:
            # TODO: SQL injection var
            sorgu = "SELECT * FROM Etiketler WHERE EtiketTip={}"
            sorgu = sorgu.format(etiket_tipi)
        else:
            sorgu = "SELECT * FROM Etiketler"

        etiketler = self._db_cursor.execute(sorgu)
        return self._cevap_olustur(etiketler)

    def post(self):
        pass

    def _cevap_olustur(self, cevap):
        """
        get HTTP sorgusuna veritabanının oluşturduğu cevaba göre cevap 
        oluşturan metoddur.

        Parametreler:
            -> cevap: Veritabanının oluşturulan sorguya verdiği cevap. 
        """

        # Cevaplar JSON formatına dönüştürülmek üzere listelenir. 
        etiketler = [{"rfid": i[1], "isim": i[2], "tip": i[3]} for i in cevap]
        return {"etiketler": etiketler}