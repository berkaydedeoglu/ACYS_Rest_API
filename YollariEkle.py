

def YollariEkle(api, cursor):
    import flask_restful
    import Etiketler

    
    api.add_resource(Etiketler.Etiketler, "/etiketler",
                    "/eiketler/<etiket_tipi>",
                    resource_class_kwargs={"cursor": cursor})
    

    
    
    
