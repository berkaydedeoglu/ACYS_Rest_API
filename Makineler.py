from flask_restful import Resource

class Makineler (Resource):
    def __init__(self, database):
        Resource()
        self.database = database
    
    def get(self):
        return "passed"

    
    def cevap_olustur(self, db_cevap: tuple)-> dict:
        pass