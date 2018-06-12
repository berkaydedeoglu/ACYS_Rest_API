

def YollariEkle(api, cursor):
    import flask_restful

    import Etiketler
    api.add_resource(Etiketler.Etiketler, "/etiketler",
                    "/etiketler/<etiket_tipi>",
                    resource_class_kwargs={"cursor": cursor[0]})
    

    import Makineler
    api.add_resource(Makineler.Makineler, "/makineler",
                    resource_class_kwargs={"cursor": cursor[0]})

    import OlayKaydi
    api.add_resource(OlayKaydi.OlayKaydi, "/olaylar",
                    "/olaylar/<int:yil>",
                    "/olaylar/<int:yil>/<int:ay>",
                    "/olaylar/<int:yil>/<int:ay>/<int:gun>",
                    resource_class_kwargs={"cursor": cursor[1]}) 
    
