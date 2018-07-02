import requests
import datetime
import time

i = 0
while True:
    i += 1
    r = requests.post("http://192.168.0.72/olaylar", data={"makine_adi": "TEZGAH 1",
                                                           "zaman": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                           "olay": "Çözgü değişti",
                                                           "makine_kodu": "axBdcf",
                                                           "cihaz_tipi": "1",
                                                           "cihaz_adi": "Çözgü 1",
                                                           "cihaz_rfid": "1274638462b47vc00008364830", })
    print(i, ". ", r.status_code, r.reason)
    # time.sleep(0.1)
