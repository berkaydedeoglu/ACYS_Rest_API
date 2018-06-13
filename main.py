from flask import Flask, request, render_template
from flask_restful import Api, Resource
import YollariEkle
import pyodbc as db


app = Flask(__name__)
api = Api(app)

database1 = db.connect(r'DRIVER={SQL SERVER};'
            r'SERVER=localhost;'
            r'DATABASE=RFIDEtiket;'
            r'UID=sa;'
            r'PWD=Berkay.97;')

database2 = db.connect(r'DRIVER={SQL SERVER};'
            r'SERVER=localhost;'
            r'DATABASE=DokumaSimulasyon;'
            r'UID=sa;'
            r'PWD=Berkay.97;')

cursor1 = database1.cursor()
cursor2 = database2.cursor()

@app.route("/")
def start():
    return render_template("Hosgeldin.html")

if __name__ == "__main__":
    
    YollariEkle.YollariEkle(api, (database1, database2))
    app.run(port=80, debug=True)
