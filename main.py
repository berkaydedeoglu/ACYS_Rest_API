from flask import Flask, request, render_template
from flask_restful import Api, Resource
import YollariEkle
import pyodbc as db

app = Flask(__name__)
api = Api(app)

# Veritabanlarına erişimi sağlayan kodlar. Gerçek senaryoda veritabanlarına
# erişim bu şekilde açıktan yapılmamalıdır.
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


@app.route("/")
def start():
    """API'ya ilk bağlanıldığında API kullanıcıyı dökümantasyon
    ile karşılar. Dökümantasyon, ./templates/ içinde 
    Hoşgeldin.html'de bulunur.

    APInin geri kalanında endpointler ./YollariEkle.py modülünde
    eklenir.
    """
    return render_template("Hosgeldin.html")


if __name__ == "__main__":

    # Tüm endpointler eklenir. Enpointlerin çalışması için oluşturulan
    # veritabanı referansları iletilir.
    YollariEkle.YollariEkle(api, (database1, database2))

    # Sunucu istenilen prottan dinlemeye başlar
    app.run(host="192.168.0.72", port=80, debug=True)
