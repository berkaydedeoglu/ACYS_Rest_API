import requests 
import datetime
import time

i = 0
while True:
    i += 1
    r = requests.post("http://192.168.0.72/olaylar", data={"makine": "TEZGAH 1", "zaman": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "mesaj": "Çözgü değişti"})
    print(i, ". ",r.status_code, r.reason)
    # time.sleep(0.5)
    