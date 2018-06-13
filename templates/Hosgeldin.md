# ACYSRest
İletişim Yazılım ACYS yazılımı için yazılmış veritabanlarına uzaktan soyutlanmış erişim sağlayan RESTful api. 

## Kullanılabilir Yollar 

### [Makineler](./makineler)
#### get:
Veritabanında kayıtlı kullanılabilir paketlerin tam listesini JSON formatında döndürür.


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

### [Kayıtlı Olaylar](./olaylar)
#### get:
Veritabanına yazılmış tüm olayları döndürür. Çok fazla kayıt varsa yavaş çalışabilir
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

