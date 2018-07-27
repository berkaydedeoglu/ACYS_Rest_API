from flask_restful import Resource
from endpoints import IsEmirleri
from bin import Optimizer

class Optimizasyon(Resource):
    def __init__(self, database):
        self.is_emirleri = IsEmirleri.IsEmirleri(database) 
        self.optimizer = Optimizer.Optimizer(self.is_emirleri) 
    
    def get(self, tezgah=None, meydanci=None, sehpa=None, is_bagi=None):
        self.optimizer.gercege_donustur(self.optimizer.optimize(tezgah, meydanci, sehpa, is_bagi))

        return self.is_emirleri.get()
