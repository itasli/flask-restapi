import json
import requests as r

f = open('data.json')
mydata = json.load(f)


f = open('address.json')
address = json.load(f)
param = "/ws/topic"


# on recupere les différents topics des serveurs, puis on boucle pour recuprer tout ce qu'on a pas en local
# il y a différent try except pour gerer les erreurs de connexion etc
# ça permet de ne pas tout planter si un serveur est down ou qu'il une donnée mal formaté
# les données servie par notre serveur sont donc safe
for i in address:
    try:
        resp = r.get(i+param+"s")
        resp.raise_for_status() 
    except r.HTTPError as exception:
        print(exception)
        continue
    
    keys = resp.json()

    for j in keys:
        try:
            resp = r.get(i+param+"/"+j)
            resp.raise_for_status() 
        except r.HTTPError as exception:
            print(exception)
            continue
        
        if j not in mydata["topics"]:
            mydata["topics"][j] = resp.json()
        
        else:

            subkeys = resp.json()
            
            for k in subkeys:
                try:
                    resp = r.get(i+param+"/"+j+"/"+k)
                    resp.raise_for_status() 
                except r.HTTPError as exception:
                    print(exception)
                    continue
                
                if k not in mydata["topics"][j]:
                    mydata["topics"][j][k] = resp.json()
                
                else:
                    mydata["topics"][j][k] = list(set(mydata["topics"][j][k] + resp.json()))

#dump to t2.json
with open('data.json', 'w') as outfile:
    json.dump(mydata, outfile, indent=4)






# recuperation des adresses des autres serveurs, on verifie qu'elles sont a minima bien formaté puis on les ajoute a la liste des adresses
# ces addresse seront utilisé pour recuperer les topics des autres serveurs lors du prochain run
new_address = []
for i in address:
    try:
        resp = r.get(i+"/ws/annuaire")
        resp.raise_for_status()
    except r.HTTPError as exception:
        print(exception)
        continue

    for j in resp.json():
        j = j.split("\"")
        for k in j:
            if "http" in k:
                j = k
        if j not in address:
            if "http" in j:
                new_address.append(j)

address = list(set(address+new_address))

with open('address.json', 'w') as outfile:
    json.dump(address, outfile)
