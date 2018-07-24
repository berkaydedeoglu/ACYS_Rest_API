# ACYSRest
İletişim Yazılım ACYS yazılımı için yazılmış veritabanlarına uzaktan soyutlanmış erişim sağlayan RESTful api. 

**Tüm veriler klasik JSON formatında alınıp okunur. Klasik http bağlantısı kurabilirsiniz. (port:80)**

  

## Kullanılabilir Yollar 

### [Makineler](./makineler)
#### get:
Veritabanında kayıtlı kullanılabilir paketlerin tam listesini JSON formatında döndürür.

---
---

### [Etiketler](./etiketler)
#### get:
Veritabanına kaydedilmiş tüm etiketleri JSON formatında döndürür.
##### Kullanılabilir Özellikler:
* **./etiketler/<int: tip>:** Etiketlerin tipine göre sorgu yapılmasını sağlar.

    ```
    ./etiketler/9 ::: Tüm "iş bağı" cihazlarını gösterir. 
    (iş bağı tip numarası 9'dur)
    
    ./etiketler/1 ::: Tüm "çözgü" cihazlarını gösterir. 
    (çözgü tip numarası 9'dur)
    ```

---
---

### [Kayıtlı Olaylar](./olaylar)
#### get:
Veritabanına yazılmış tüm olayları döndürür. Çok fazla kayıt varsa yavaş çalışabilir 

*(GELİŞTİRME NOTU: Sayfalandırma yapılabilir.)*
*(GELİŞTİRME NOTU: Büyük verilerde veri kullanımından tasarruf için çözgü adı makine adı gibi veriler kaldırılıp ilişkisel yolla bağlanabilir.*

##### Kullanılabilir Özellikler:
* **./olaylar/<int: yil>:** İlgili yıla göre sorgu yapılır.
	```
	./olaylar/2012 ::: 2012 yılına ait olayları gönderir.
	```
* **./olaylar/<int: yil>/<int: ay>:** İstenilen yıl ve aya göre sogu yapılır.
		
	```
	./olaylar/2012/06 ::: 2012 yılının 6. ayına göre sorgu yapılır.
	``` 

* **./olaylar/<int: yil>/<int: ay>/<int: gun>** : İstenilen yıl,  ay ve güne göre arama yapılır.

	```
	./olaylar/2012/06/17 ::: 2012 yılının 6. ayının 17. gününe göre sorgu yapılır.
	```

#### post:
Veritabanına yeni olay yazar. Aldığı veriler:
* **makine_adi**: Değişiklik olan makinenin adı
* **makine_kodu**: Değişiklik olan makinenin sistem kodu
* **olay**: Değişiklik mesajı
* **cihaz_tipi**: Makineye bağlanan ya da sökülen cihazın tip numarası.
* **cihaz_adi**: Makineye bağlanan cihazın okunabilir adı.
* **cihaz_rfid**: Bağlanan cihazın etiket kodu. 
* **zaman**: Değişiklik yapılma zamanı (datetime tipinde "yyyy-MM-dd hh.mm.ss" formatında olmalıdır)

	```
	post : ./olaylar  data={"makine_adi": "TEZGAH 1",
					"zaman": "21.06.2018 06:58:34.000
					"olay": "Çözgü değişti",
					"makine_kodu": "axBdcf",
					"cihaz_tipi": "1",
					"cihaz_adi": "Çözgü 1",
					"cihaz_rfid": "1274638462b47vc00008364830", })
	```
---
---

### [Anlık Olaylar](./anlikolaylar)

Anlık olay oluşumlarının izlenebildiği yoldur. Makineye çözgü bağlanması, cihazların izlenmesi istenen olaylar bu yoldan ulaşılabilir.

**NOT:** Bu endpoint veritabanıyla hiçbir durumda haberleşmez.  Veriler daima bulunan makinenin RAM'inde tutulur. Bu yüzden yazılan veriler geçicidir. 

Şimdilik sadece makine olaylarını gösteriyor. Örnek bir makine olayı:

```
{
  "olaylar": [
    {
      "olay": "degisim_basladi",
      "mesaj": "Bağlanma bekleniyor",
      "zaman": "19.06.2018 01:57",
      "makine": "TEZGAH 1"
    }
  ]
}
```

Bu endpoint,  projedeki tüm alanların birbirleri ile haberleşmesi için oluşturulmuştur. Bu yüzden bir olaydaki anahtar sözcüklerin nasıl seçileceği haberleşecek iki ucun anlaşmalarına bağlıdır.

Örneğin C# Desktop Cilent ve Android Client uç tarafları çözgü değişiminin başladığını belirtmek için **olay** anahtar sözcüğünü kullanırlar. Yukarıdaki örnekte çözgü değişiminin başladığını ifade etmek için *degisim_basladi* etiketi kullanılmıştır. İki taraf da bu etiketi dinler.

#### get:

Sistemde o  anda yazılmış olayların tamamını listeler.  Olayları dinleyen tarafta kullanılır.

**NOT:** Şimdilik sadece makine olaylarını desteklemektedir. Her makine için karışıklığı önlemek ve performansı artırmak için maksimum 1 olay tutulur.  

#### post:

Sisteme bir olay ekler. Olayları gönderecek tarafta kullanılır. Alınan veriler:

* **olay:** Olay kodu. Tarafların haberleşmede kullandığı kodlar.
* **mesaj:** Olayla birlikte gönderilen mesaj.
* **zaman:** Olayın gerçekleşme zamanı. 
* **makine:** Olayın gerçekleştiği makine. (Makine kodu da olabilir)  

---
---

### [İş Emirleri](./isemirleri):

CoralReef  yazılımının oluşturduğu iş emirleri tablosunun tüm satırlarını listeler. Listelenen sütunlar:


  - **Operation.OID** : Benzersiz operasyon ID'si. (_olay_id_)
  - **Operation .Name**:  İşin adı (_olay_isim_)
  - **WorkOrder.PlanningBeginTime**: İşin planlanan başlama zamanı. (_planlanan_baslangic_)
  - **WorkOrder.PlanningEndTime**: İşin planlanan bitiş zamanı. (_planlanan_bitis_)
  - **WorkOrder.ActualBeginTime**: İşin gerçekte başladığı an (_gercek_baslangic_)
  - **WorkOrder.ActualEndTime**: İşin gerçekte tamamlandığı an (_gerçek_bitis_)
  - **WorkOrder.RunTime**: Planlanan zamanlara göre saniye cinsinden zaman. (_calisma_zamani_)
  - **WorkOrder.HeadTime** : İşin gerçek zamanlı saniye cinsinden süresi. Dinamik. (_bitis_gecikme_)
  - **WorkOrder.TailTime** : İşin diğer işler yüzünden toplam gecikmesi. Dinamik. (_baslangic_gecime_)

**Geliştirici Notu:** İşlerin saniye cinsinden anlık değişimlerinin tutulması API kullanan clientler tarafından zorunlu olmasa da işleri kolaylaştırdığından ve istemcilerin yorumlama değil sadece gösterim yapma fikrine daha uygun olduğundan kullanılmıştır. Yapılan testlerde bu ekstra sütunların tutulması ve dinamik olarak değiştirilmesi çok çok küçük farklar oluşturduğundan görmezden gelinmiştir.

Dinamik bilgiler anlık olarak (istenilen sürede bir) güncellenir. Güncellenme olayları ise anlık olaylar endpointinden sağlanır. Yani anlık olaylara gönderdiğiniz bir değer bu endpointi de etkileyebilir.    

Güncellenme sıklığını settings.br dosyasından değiştirebilirsiniz. (_IS_EMIRLERI_GUNCELLEME_SURESI_)

 

