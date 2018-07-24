from endpoints import IsEmirleri, AnlikOlay
import time, threading

class IsEmriGuncelleyici(threading.Thread):
    """
    Veritabanında iş emirlerini dinamik olarak güncelleyen ve anlık olayları 
    izleyen sınıf
    """


    def __init__(self, db):
        super().__init__()
        
    def uyar(self, makine, olay):
        pass

    def run(self):
        pass
    

