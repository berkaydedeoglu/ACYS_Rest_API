from flask_restful import Resource, reqparse


class AnlikOlay(Resource):

    _olaylar = []

    def __init__(self):
        self._parametreler = reqparse.RequestParser()

    def get(self):
        return {"olaylar": self._olaylar}, 200

    def post(self):
        self._parametreler.add_argument("olay")
        self._parametreler.add_argument("mesaj")
        self._parametreler.add_argument("zaman")
        self._parametreler.add_argument("makine_id")

        args = self._parametreler.parse_args()

        m = self.makineyi_bul(args["makine"].strip())

        if m != -1:
            m["olay"] = args["olay"]
            m["mesaj"] = args["mesaj"]
            m["zaman"] = args["zaman"]
            m["makine_id"] = args["makine_id"].strip()

        else:
            self._olaylar.append({
                "olay": args["olay"],
                "mesaj": args["mesaj"],
                "zaman": args["zaman"],
                "makine_id": args["makine_id"].strip()
            })

        return 200

    def makineyi_bul(self, makine_id):
        for i in self._olaylar:
            if i["makine_id"] == makine_id:
                return i

        return -1
