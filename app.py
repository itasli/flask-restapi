from flask import Flask, render_template
from flask_restful import Api
from ressources.ws import Ws
from ressources.annuaire import Annuaire
from json import load

app = Flask(__name__)
api = Api(app)

    
# on initialise les deux "endpoint"
api.add_resource(Ws, '/ws/topics/', '/ws/topic/<string:sub1>/', '/ws/topic/<string:sub1>/<string:sub2>/')
api.add_resource(Annuaire, '/ws/annuaire/')


    
@app.route('/')
def accueil():
    
    # a chaque fois je recalcul la liste des différent topic que j'ai pour les ajouter a la page d'acceuil
    # Todo: implementer le hash et verifier si une donnée à bouger depuis le dernier calcul ?
    # Todo: affichier les serveur auquel on est connecté, dans le meme esprit que les topics pas très difficile
    f = open('data.json')
    data = load(f)
    keys = list(data["topics"].keys())
    return render_template('accueil.html', len=len(keys), keys=keys)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

    # le dossier common contient les fichiers de configuration et de connexion a mongodb
    # qui est finalement pas utilisé.