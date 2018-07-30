from flask_restful import Resource
from endpoints import IsEmirleri
from bin import Optimizer

class Optimizasyon(Resource):
    def __init__(self, database, y_database):
        self.is_emirleri = IsEmirleri.IsEmirleri(database) 
        self.optimizer = Optimizer.Optimizer(self.is_emirleri) 

        
        self.y_database = y_database
    
    def get(self, tezgah=4, meydanci=1, sehpa=1, is_bagi=1):
        self.kaynaklari_kaydet(tezgah, meydanci,sehpa, is_bagi)

        self.optimizer.gercege_donustur(self.optimizer.optimize(tezgah, meydanci, sehpa, is_bagi))

        return self.is_emirleri.get()
    
    def kaynaklari_kaydet(self, tezgah, meydanci, sehpa, is_bagi):
        y_cursor = self.y_database.cursor()
        y_cursor.execute("UPDATE Kaynaklar SET TezgahSayisi={}, MeydanciSayisi={}, SehpaSayisi={}, IsBagiMakinesiSayisi={}".format(tezgah,
        meydanci, sehpa, is_bagi))

        self.y_database.commit()
