from flask import Flask, request, render_template
from flask_restful import Api, Resource
import YollariEkle
import pyodbc as db


app = Flask(__name__)
api = Api(app)

database = db.connect(r'DRIVER={SQL SERVER};'
            r'SERVER=localhost;'
            r'DATABASE=RFIDEtiket;'
            r'UID=sa;'
            r'PWD=Berkay.97;')
cursor = database.cursor()

@app.route("/")
def start():
    return render_template("start.html")

if __name__ == "__main__":
    

    YollariEkle.YollariEkle(api, cursor)
    app.run(host="192.168.0.72", port=5001)
