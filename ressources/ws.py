from flask_restful import Resource
from json import load
#from bson.json_util import dumps, loads
#from common.util import mongodb


class Ws(Resource):

    def get(self, sub1=None, sub2=None):
        
        """ cursor = mongodb["ws"].find({}, {'_id': False})
        list_cur  = list(cursor)
        json_data = dumps(list_cur)
        json_data = loads(json_data)[0] """
        
        f = open('data.json')
        json_data = load(f)

        if sub2 is not None:
            try:
                json_data = json_data["topics"][sub1][sub2]
            except Exception as e:
                #on veille a bien retourner une erreur 404 si la donnée n'est pas trouvée ou qu'ils y a un problème
                return {"error": f"{e} not found"}, 404
        
        elif sub1 is not None:
            try:
                json_data = json_data["topics"][sub1]
            except Exception as e:
                #on veille a bien retourner une erreur 404 si la donnée n'est pas trouvée ou qu'ils y a un problème
                return {"error": f"{e} not found"}, 404
    
        else:
            try:
                json_data = list(json_data["topics"].keys())
            except Exception as e:
                #on veille a bien retourner une erreur 404 si la donnée n'est pas trouvée ou qu'ils y a un problème
                return {"error": f"{e} not found"}, 404
        
        return json_data