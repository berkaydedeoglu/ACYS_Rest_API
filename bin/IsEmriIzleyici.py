from endpoints import AnlikOlay, IsEmirleri
import threading, time

class IsEmriIzleyici(threading.Thread):

    def __init__(self, db):
        super().__init__()
        self.anlik_is_emri = None
        self._index = -1
        self.is_emirleri_cls = IsEmirleri.IsEmirleri(db)
        self.is_emirleri = self.is_emirleri_cls.get()["is_emirleri"]
        self.kullanilmis_emirler = []
        self.bayrak = False
        self.timer = None
        self.thread_bayrak = True

    def durdur(self):
        self.thread_bayrak = False

    def diger_operasyon(self, zaman):
        if self.anlik_is_emri:
            self.is_emirleri_cls.set_gercek_bitis(self.anlik_is_emri["emir_id"], zaman)
        self.kullanilmis_emirler.append(self.anlik_is_emri)
        self._index += 1
        self.anlik_is_emri = self.is_emirleri[self._index]

        self.is_emirleri_cls.set_gercek_baslangic(self.anlik_is_emri["emir_id"], zaman)
        self.timer = time.clock()


    def anlik_olay_kontrol(self):
        anlik_olaylar = AnlikOlay.AnlikOlay().get()[0]["olaylar"]

        if not anlik_olaylar:
            return -1

        olay = anlik_olaylar[0]


        if olay["olay"] == "cozgu_bitti":
            # Çözgü taşıma operasyonu başlamıştır.
            # Manual sinyal
            if not self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = True
        elif olay["olay"] == "yeni_cozgu_geldi":
            # Çözgü taşıma operasyonu bitmiştir.
            # Çözgü takılma operasyonu başlamıştır.
            if self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = False
        elif olay["olay"] == "eski_cozgu_gitti":
            # Çözgü takılma operasyonu bitmiştir.
            # Sehpa taşıma operasyonu başlamıştır.
            if not self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = True
        elif olay["olay"] == "sehpa_geldi":
            # Sehpa bağlanmıştır.
            # Sehpa çözgü bağlama operasyonu başlamıştır.
            if self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = False
        elif olay["olay"] == "is_bagi_geldi":
            # Önceki operasyon tamamlanmıştır.
            # İş bağı bitişi operasyonu başlamıştır.
            if not self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = True
        elif olay["olay"] == "sehpa_ayrildi":
            # iş bağı ve sehpa ayrılmıştır.
            # Ayar yapılması operasyonu başlamıştır.
            if self.bayrak:
                self.diger_operasyon(olay["zaman"])
            self.bayrak = False
        elif olay["olay"] == "degisim_bitti":
            # Değişim tamamlanmıştır
            # Kullanılmışları temizle
            self._index = -1

    def run(self):

        while self.thread_bayrak:
            # Şu anki iş emrini seçer
            self.anlik_olay_kontrol()

            # İş Emirlerinin güncel halini yeniden alır
            self.is_emirleri = self.is_emirleri_cls.get()["is_emirleri"]

            if not self.anlik_is_emri:
                time.sleep(5)
                continue

            timer2 = time.clock()

            diff = int(timer2-self.timer)

            # Başlangıç zamanından itibaren geçen süre yazılır.
            self.is_emirleri_cls.set_baslangic_gecikme(self.anlik_is_emri["emir_id"], diff)

            if diff > self.anlik_is_emri["calisma_zamani"]:

                for i in self.is_emirleri[self._index+1:]:
                    gecikme = (diff - self.anlik_is_emri["calisma_zamani"]) + self.anlik_is_emri["bitis_gecikme"]
                    self.is_emirleri_cls.set_bitis_gecikme(i["emir_id"], gecikme)

            time.sleep(10)
