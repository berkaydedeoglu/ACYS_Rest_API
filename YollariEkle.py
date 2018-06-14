

def YollariEkle(api, databases):
    import flask_restful

    from endpoints import Etiketler
    api.add_resource(Etiketler.Etiketler, "/etiketler",
                    "/etiketler/<etiket_tipi>",
                    resource_class_kwargs={"database": databases[0]})
    

    from endpoints import Makineler
    api.add_resource(Makineler.Makineler, "/makineler",
                    resource_class_kwargs={"database": databases[0]})

    from endpoints import OlayKaydi
    api.add_resource(OlayKaydi.OlayKaydi, "/olaylar",
                    "/olaylar/<int:yil>",
                    "/olaylar/<int:yil>/<int:ay>",
                    "/olaylar/<int:yil>/<int:ay>/<int:gun>",
                    resource_class_kwargs={"database": databases[1]}) 
    
