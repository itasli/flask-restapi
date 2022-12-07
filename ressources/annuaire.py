from flask_restful import Resource
from json import load

class Annuaire(Resource):

    def get(self):
        f = open('address.json')
        data = load(f)
        return data
        