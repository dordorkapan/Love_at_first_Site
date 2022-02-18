# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 11:30:33 2022

@author: user
"""

from flask import *
import sqlite3

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Dora', password='12345'))
users.append(User(id=2, username='Elisa', password='test'))
users.append(User(id=3, username='Hind', password='password'))


# Fonctions utilisées pour appeler des commandes SQL
def lire_base():
    """ Récupére des personnes dans la table
        Renvoie (list of tuples) : liste des personnes
    """
    connexion = sqlite3.connect("base_CNRS.sqbpro")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT *
    FROM Abonnes;"""
    resultat = curseur.execute(requete_sql)
    personnes = resultat.fetchall()
    connexion.close()
    return personnes

def index_max():
    """ Récupére l'id du prochain enregistrement
        Renvoie un entier
    """
    connexion = sqlite3.connect("base_CNRS.sqbpro")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT MAX(id)
    FROM Abonnes;"""
    resultat = curseur.execute(requete_sql)
    index = resultat.fetchall()
    connexion.close()
    return int(index[0][0])+1 # Transtype le résultat de la recherche et ajoute 1


def recherche_sql(donnees):
    """
    Recherche au moins une des informations comprise dans le dictionnaire donnees
    Si un élément est nul, alors le paramètre de la recherche est vide
    Sinon, il est de la forme: '%'+element+'%'
    """
    parametre0, parametre1, parametre2, parametre3, parametre4, parametre5 = "", "", "", "", "", ""
    if donnees['pronoms'] !="":
        parametre0 = '%'+donnees['Pronoms']+'%'
    if donnees['age'] != "":
        parametre1 = '%'+donnees['Age']+'%'
    if donnees['ville'] != "":
        parametre2 = '%'+donnees['ville']+'%'
    if donnees['colOeil'] != "":
        parametre1 = '%'+donnees['yeux']+'%'
    if donnees['colChev'] != "":
        parametre2 = '%'+donnees['cheveux']+'%'
    if donnees['hauteur'] !="":
        parametre0 = '%'+donnees['hauteur']+'%'
    parametres = (parametre0, parametre1, parametre2, parametre3, parametre4, parametre5)
    connexion = sqlite3.connect("base_CNRS.sqbpro")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT *
    FROM Abonnes 
    WHERE pronoms LIKE ? OR age LIKE ? OR ville LIKE ? OR colOeil LIKE ? OR colChev LIKE ? OR hauteur LIKE ?;"""
    resultat = curseur.execute(requete_sql, parametres)
    abonnes = resultat.fetchall()
    connexion.close()
    return abonnes


def ajoute_enregistrement(indice, donnees):
    """ Créé l'enregistrement avec le nouvel id et les données saisies
        Renvoire un booléen : True si l'ajout a bien fonctionné
    """
    # Test si tous les champs sont renseignés
    parametre0 = donnees['username']
    parametre1 = donnees['nom']
    parametre2 = donnees['prenom']
    parametre3 = donnees['pronouns']
    parametre4 = donnees['age']
    parametre5 = donnees['ville']
    parametre6 = donnees['colOeil']
    parametre7 = donnees['colChev']
    parametre8 = donnees['hauteur']
    parametre9 = donnees['1date']
    parametre10 = donnees['laSolution']
    parametre11 = donnees['hobby']
    parametre12 = donnees['insta']
    if parametre0 == "" or parametre1 == "" or parametre2 == "" or parametre3 == "" \
        or parametre4 == "" or parametre5 == "" or parametre6 == "" or parametre7 == "" \
        or parametre8 == "" or parametre9 == "" or parametre10 == "" or parametre11 == "" \
        or parametre12 == "" or parametre13 == "":
        return False
    parametres = (indice, parametre0, parametre1, parametre2)
    connexion = sqlite3.connect("base_CNRS.sqbpro")
    curseur = connexion.cursor()
    requete_sql = """
    INSERT INTO Labos (id, nom, prenom, pronouns, age, ville, colOeil, colChev, hauteur, 1date, laSolution, hobby, insta ) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    resultat = curseur.execute(requete_sql, parametres)
    connexion.commit()
    connexion.close()
    return True




# Création d'un objet application web Flask
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'somesecretkeythatonlyishouldknow'



@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
# Création d'une fonction log_in() associee a l'URL "/"
# pour générer une page web dynamique
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
    
        username = request.form['username']
        password = request.form['password']
            
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('chercher'))
    
            return redirect(url_for('login'))
    
    # Si vous cliquez sur "abonner", vous accédez à la page "/abonnement"
    #if...
        #return redirect(url_for('abonner'))
    
    return render_template("1log-in.html")

@app.route("/abonnement")
def abonner():
    return render_template("2abonnement.html")

# Page utilisant une base de données
@app.route("/chercher", methods = ['GET','POST'])
def chercher():
    return render_template("3cherche_l'amour.html")

@app.route("/liste_matchs", methods = ['GET','POST'])
def liste_matchs():
    result = request.form # Récupération des informations en provenance du POST: C'est un dictionnaire
    liste_match = bdd.lire_base(result)
    return render_template("4list_matchs.html", nom = result['NOM'], \
           prenom = result['PRENOM'], pronuns = result['PRONOM'], \
           ville = result['VILLE'], age = result['AGE'], colOeil = result['COULEUR DES YEUX'], \
           colChev = result['COULEUR DE CHEVEUX'], hauteur = result['HAUTEUR'],\
           firstDate = result['IDÉE DE PREMIER SORTIE IDÉAL'], hobby = result['HOBBIES'], \
           laSolution = result['LA SOLUTION'], insta = result['INSTAGRAM'], abonnes = liste_match)

if __name__ == "__main__":
    app.run(port=1660)
    
    
 
