# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 11:30:33 2022

@author: user
"""

from flask import *
#from flask_mysqldb import MySQL
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
#mysql = MySQL()
app = Flask(__name__, static_url_path='/static')


def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['MYSQL_DB'] = 'flask'
    
    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Fonctions utilisées pour appeler des commandes SQL
def lire_base():
    """ Récupére des personnes dans la table
        Renvoie (list of tuples) : liste des personnes
    """
    connexion = sqlite3.connect("bdd/base_CNRS.sqbpro")
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
    connexion = sqlite3.connect("bdd/base_CNRS.sqbpro")
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
    if donnees['pronouns'] !="":
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
    connexion = sqlite3.connect("bdd/base_CNRS.sqbpro")
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
    connexion = sqlite3.connect("bdd/base_CNRS.sqbpro")
    curseur = connexion.cursor()
    requete_sql = """
    INSERT INTO Labos (id, nom, prenom, pronouns, age, ville, colOeil, colChev, hauteur, 1date, laSolution, hobby, insta ) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    resultat = curseur.execute(requete_sql, parametres)
    connexion.commit()
    connexion.close()
    return True



# Création d'une fonction log_in() associee a l'URL "/"
# pour générer une page web dynamique

@app.route('/')
def login():
    return render_template('1log-in.html')

@app.route('/', methods=['POST'])
def login_post():
     #le code de connexion va ici
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # vérifier si l'utilisateur existe réellement
    # prendre le mot de passe fourni par l'utilisateur, le hacher et le comparer au mot de passe haché dans la base de données
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('app.login')) # si l'utilisateur n'existe pas ou si le mot de passe est erroné, rechargez la page
    # si la vérification ci-dessus réussit, nous savons que l'utilisateur dispose des bonnes informations d'identification
    login_user(user, remember=remember)
    return redirect(url_for('chercher'))

@app.route("/abonnement")
def abonner():
    return render_template("2abonnement.html")

@app.route('/abonnement', methods=['POST'])
def abonner_post():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("L'adresse du nom d'utilisateur existe déjà")
        return redirect(url_for('app.abonner'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('app.login'))

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
    
    
 