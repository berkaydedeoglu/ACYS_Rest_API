from bin import ZamanSimulasyonu
import pyodbc as db

database2 = db.connect(r'DRIVER={SQL SERVER};'
                       r'SERVER=localhost;'
                       r'DATABASE=DokumaSimulasyon;'
                       r'UID=sa;'
                       r'PWD=Berkay.97;')

database3 = db.connect(r'DRIVER={SQL SERVER};'
                       r'SERVER=localhost;'
                       r'DATABASE=CoralReef_Ersan2;'
                       r'UID=sa;'
                       r'PWD=Berkay.97;')

zs = ZamanSimulasyonu.ZamanSimulasyonu(database3, database2)
print(zs.kaynaklar)
print(zs.mutlak_zaman)

