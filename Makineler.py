from flask_restful import Resource

class Makineler (Resource):
    def __init__(self, cursor):
        Resource()
    
    def get(self):
        return "passed"

    
    def cevap_olustur(self, db_cevap: tuple)-> dict:
        pass