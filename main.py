from flask import Flask, request, render_template
from flask_restful import Api, Resource
import pyodbc as db
from bin import IsEmriIzleyici, AyarOkuyucu, YollariEkle

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

database3 = db.connect(r'DRIVER={SQL SERVER};'
                       r'SERVER=localhost;'
                       r'DATABASE=CoralReef_Ersan;'
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

    # Ayarlar okunur ve atanır.
    ayar_okuyucu = AyarOkuyucu.AyarOkuyucu()
    ip = ayar_okuyucu.ayar("IP_ADRESS")
    port = ayar_okuyucu.ayar("PORT")

    # Tüm endpointler eklenir. Enpointlerin çalışması için oluşturulan
    # veritabanı referansları iletilir.
    YollariEkle.YollariEkle(api, (database1, database2, database3))

    # Ağ trafikteki gerekli bilgiler izlenir. İş emirleri güncellenir.
    izleyici = IsEmriIzleyici.IsEmriIzleyici(database3)
    izleyici.start()

    # Sunucu istenilen porttan dinlemeye başlar
    app.run(ip, port, debug=True)
