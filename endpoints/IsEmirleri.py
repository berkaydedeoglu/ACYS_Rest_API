from flask_restful import Resource
import datetime

class IsEmirleri(Resource):
    def __init__(self, database):
        super()
        self._db = database
        self. _cursor = database.cursor()

    def get(self):
        sorgu = """SELECT W.OID, O.OID, O.Name, W.PlanningBeginTime,
                    W.PlanningEndTime, W.ActualBeginTime,
                    W.ActualEndTime, W.RunTime, W.HeadTime, W.TailTime
                    FROM WorkOrder as W JOIN Operation as O ON O.OID = W.OperationID"""

        db_cevap = self._cursor.execute(sorgu)

        return self.cevap_olustur(db_cevap)

    def cevap_olustur(self, db_cevap):
        return {"is_emirleri": [{
            "emir_id": i[0],
            "olay_id": i[1],
            "olay_isim": i[2],
            "planlanan_baslangic" : str(i[3]),
            "planlanan_bitis" : str(i[4]),
            "gercek_baslangic" : str(i[5]),
            "gercek_bitis" : str(i[6]),
            "calisma_zamani" : i[7],
            "bitis_gecikme" : i[8],
            "baslangic_gecikme" : i[9]} for i in db_cevap]}

    def set_gercek_baslangic(self, emir_id, zaman):
        dt = datetime.datetime.strptime(zaman[:19], '%Y-%m-%d %H:%M:%S')
        sorgu = "UPDATE WorkOrder set ActualBeginTime=convert(datetime, '{}') WHERE OID={}".format(zaman, emir_id)
        self._cursor.execute(sorgu)
        self._db.commit()


    def set_gercek_bitis(self, emir_id, zaman):
        dt = datetime.datetime.strptime(zaman[:19], '%Y-%m-%d %H:%M:%S')
        sorgu = "UPDATE WorkOrder set ActualEndTime=convert(datetime, '{}') WHERE OID={}".format(zaman, emir_id)
        self._cursor.execute(sorgu)
        self._db.commit()

    def set_bitis_gecikme(self, emir_id, zaman):
        sorgu = "UPDATE WorkOrder set HeadTime={} WHERE OID={}".format(zaman, emir_id)
        self._cursor.execute(sorgu)
        self._db.commit()

    def set_baslangic_gecikme(self, emir_id, zaman):
        sorgu = "UPDATE WorkOrder set TailTime={} WHERE OID={}".format(zaman, emir_id)
        self._cursor.execute(sorgu)
        self._db.commit()
