singleton_flag = None

def singleton(cls):
    global singleton_flag

    def check():
        global singleton_flag
        if singleton_flag:
            return singleton_flag
        else:
            singleton_flag = cls()
            return singleton_flag

    return check

@singleton
class AyarOkuyucu:
    def __init__(self):
        self.ayarlar = {}
        self.parse()

    def parse(self):
        with open("settings.br", "r") as dosya:
            for satir in dosya:
                kv = [i.strip() for i in satir.split("=")]

                # Satır eğer istenilen formattaysa 2 uzunlukludur.
                # Eğer 2 uzunluklu değilse istenmeyen bir formatta
                # ya da yorum satırıdır.
                if len(kv) != 2:
                    continue

                self.ayarlar[kv[0]] = kv[1]

    def ayar(self, ayar):
        return self.ayarlar[ayar]


if __name__ == "__main__":
    print(AyarOkuyucu().ayar("IS_EM"))
