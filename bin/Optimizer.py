class Optimizer():
    '''
    Is Emirlerini optimize hale getirir.
    '''

    def __init__(self, is_emirleri_cls):
        self.is_emirleri_cls = is_emirleri_cls
        self.is_emirleri = self.is_emirleri_cls.get()["is_emirleri"]

    def optimize(self, tezgah, isci, sehpa, is_bagi):
        import math

        bos_isci_sayisi = isci
        sehpa_sayisi = sehpa
        is_bagi_sayisi = is_bagi
        tezgah_sayisi = tezgah
        tezgahlar = []
        sehpalar = []
        is_baglari = []

        cozgu_zaman = 900
        sehpa_zaman = 600
        is_bagi_zaman = 2400
        ayar_zaman = 1200

        anlik_zaman = 0


        for i in range(tezgah_sayisi):
            tezgahlar.append({ "cozgu_takilma": 0, "sehpa_isleme": 0, "is_bagi_isleme": 0 })

        for i in range(sehpa_sayisi):
            sehpalar.append({ "müsait_olma": 0 })

        for i in range(is_bagi_sayisi):
            is_baglari.append({ "müsait_olma": 0 })

        def en_kısa_sehpa_bul():
            en_kisa = sehpalar[0]

            for i in sehpalar:
                if i["müsait_olma"] < en_kisa["müsait_olma"]:
                    en_kisa = i

            return en_kisa

        def en_kısa_is_bagi():
            en_kisa = is_baglari[0]

            for i in is_baglari:
                if i["müsait_olma"] < en_kisa["müsait_olma"]:
                    en_kisa = i

            return en_kisa

        
 

        # Meydancılar kendi işlerini yaparlar.
        c_g_t = tezgah_sayisi  ## Çözgü gereken tezgah sayısı
        t_no = 0
        for j in range(math.ceil(tezgah_sayisi/bos_isci_sayisi)):

            for i in range(bos_isci_sayisi):

                tezgahlar[t_no]["cozgu_takilma"] = anlik_zaman
                c_g_t -= 1
                t_no += 1

                if c_g_t <= 0:
                    break
            
            anlik_zaman += cozgu_zaman


        for i in tezgahlar:
            sehpa = en_kısa_sehpa_bul()
            if i["cozgu_takilma"] + cozgu_zaman > sehpa["müsait_olma"]:
                i["sehpa_isleme"] = i["cozgu_takilma"]  + cozgu_zaman # + sehpa["müsait_olma"]
            else:
                i["sehpa_isleme"] = sehpa["müsait_olma"] # + i["cozgu_takilma"]  

            ib = en_kısa_is_bagi()
            if i["sehpa_isleme"] + sehpa_zaman > ib["müsait_olma"]: # iş bağı müsait ise
                i["is_bagi_isleme"] =   i["sehpa_isleme"] + sehpa_zaman 
            else:
                i["is_bagi_isleme"] =  ib["müsait_olma"] # + sehpa_zaman# + i["sehpa_isleme"] 
            sehpa["müsait_olma"] = i["is_bagi_isleme"] + is_bagi_zaman
            ib["müsait_olma"] = sehpa["müsait_olma"]
        
        return tezgahlar

        
    def gercege_donustur(self, tezgahlar):
        import datetime

        mutlak_baslangic = datetime.datetime.strptime(self.is_emirleri[0]["planlanan_baslangic"], "%Y-%m-%d %H:%M:%S")
        is_emirleril = self.is_emirleri

        t_no = 0
        for i in tezgahlar:

            ##################################### Çözgü Taşıma ###############################################

            is_emri    = is_emirleril[t_no*6 + 0]
            is_emri_no = is_emri["emir_id"]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=i["cozgu_takilma"])
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])
            
            
            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t\t", baslangic, bitis)

            ##################################### Çözgü Bağlama ###############################################

            is_emri = is_emirleril[t_no*6 + 1]
            e_is_emri = is_emirleril[t_no*6 + 0]
            is_emri_no = is_emri["emir_id"]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=i["cozgu_takilma"] + e_is_emri["calisma_zamani"])
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])


            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t", baslangic, bitis)

            #################################### Sehpa Taşınması ################################################

            is_emri    = is_emirleril[t_no*6 + 2]
            is_emri_no = is_emri["emir_id"]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=i["sehpa_isleme"])
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])
            

            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t\t", baslangic, bitis)
            
            ################################## Sehpa Bağlama ##################################################

            is_emri    = is_emirleril[t_no*6 + 3]
            is_emri_no = is_emri["emir_id"]
            e_is_emri = is_emirleril[t_no*6 + 2]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=(i["sehpa_isleme"] + e_is_emri["calisma_zamani"]))
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])

            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t", baslangic, bitis)


            ################################ İş Bağı İşlemi ####################################################

            is_emri    = is_emirleril[t_no*6 + 4]
            is_emri_no = is_emri["emir_id"]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=i["is_bagi_isleme"])
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])


            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t", baslangic, bitis)


            ################################ Ayar Yapılması ####################################################

            is_emri    = is_emirleril[t_no*6 + 5]
            is_emri_no = is_emri["emir_id"]
            e_is_emri = is_emirleril[t_no*6 + 4]
            baslangic  = mutlak_baslangic + datetime.timedelta(seconds=i["is_bagi_isleme"] + e_is_emri["calisma_zamani"])
            bitis      = baslangic + datetime.timedelta(seconds=is_emri["calisma_zamani"])


            self.is_emirleri_cls.set_planli_zaman(is_emri_no, baslangic, bitis)
            print(str(t_no) + ". Tezgah", is_emri["olay_isim"], "\t\t\t", baslangic, bitis)
            
            t_no += 1

            



if __name__ == "__main__":
    from endpoints import AnlikOlay, IsEmirleri

    optimizer = Optimizer(IsEmirleri.IsEmirleri())
    a = [int(i) for i in input().split()]
    optimizer.optimize(a[0], a[1], a[2], a[3])
    