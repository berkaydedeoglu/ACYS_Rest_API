from endpoints import IsEmirleri, AnlikOlay

class ZamanSimulasyonu:
    def __init__(self, coral_db, dokuma_db):
        self.is_emirleri = IsEmirleri.IsEmirleri(coral_db)
        self.olaylar = AnlikOlay.AnlikOlay()
        self.dokuma_db = dokuma_db
        
        self.anlik_zaman = 0

        self.kaynaklari_al()
        self.mutlak_zaman_ayarla()
    
    def kaynaklari_al(self):
        cur = self.dokuma_db.cursor()
        kaynaklar_list = cur.execute("SELECT TOP(1) * FROM Kaynaklar").fetchone()
        self.kaynaklar = {
            "Tezgah": kaynaklar_list[0], 'Meydanci' : kaynaklar_list[1],
            'Sehpa' : kaynaklar_list[2], 'IsBagi' : kaynaklar_list[3]
        }
    
    def mutlak_zaman_ayarla(self):
        import datetime

        IlkEmir = self.is_emirleri.get()['is_emirleri'][0]
        self.mutlak_zaman = IlkEmir['planlanan_baslangic']
        self.mutlak_zaman = datetime.datetime.strptime(self.mutlak_zaman, "%Y-%m-%d %H:%M:%S")



    def simulasyonu_baslat(self):
        pass

if __name__ == '__main__':
    import pyodbc as db

    database2 = db.connect(r'DRIVER={SQL SERVER};'
                       r'SERVER=localhost;'
                       r'DATABASE=DokumaSimulasyon;'
                       r'UID=sa;'
                       r'PWD=Berkay.97;')
    
    zs = ZamanSimulasyonu(None, database2)
    print(zs.kaynaklar)
