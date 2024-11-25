from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors
# TODO : TO REMOVE !! -----------------------
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("USERNAME")
mdp = os.getenv("MDP")
database = os.getenv("DATABASE")
# TODO : TO REMOVE !!! ---------------------
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # à modifier
            user=username,  # à modifier
            password=mdp,  # à modifier
            database=database,  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # à activer sur les machines personnelles :
        # activate_db_options(g.db)
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')


@app.route('/reduction/show', methods=['GET'])
def show_reduction():
    return render_template('reduction/show_reduction.html')


@app.route('/client/show', methods=['GET'])
def show_client():
    return render_template('client/show_client.html')


@app.route('/tri/show', methods=['GET'])
def show_tri():
    mycursor = get_db().cursor()
    sql = '''
        SELECT R.date_ramassage AS dateRamassage,
           Tri.id_ramassage AS idRamassage,
           Tri.id_type      AS idTypeVetement,
           Tv.libelle_type  AS nomTypeVetement,
           poids_type_trie  AS quantite,
           Tv.prix_kg_type  AS prixVetement
    FROM Tri
             JOIN Ramassage R on Tri.id_ramassage = R.id_ramassage
             JOIN Type_vetement Tv on Tv.id_type = Tri.id_type;
    '''
    mycursor.execute(sql)
    tris = mycursor.fetchall()
    print(tris)
    return render_template('tri/show_tri.html', tris=tris)


@app.route('/achat/show', methods=['GET'])
def show_achat():
    mycursor = get_db().cursor()
    sql = ''' SELECT Achat.id_achat AS Identifiant,
    Achat.date_achat AS Date,
    Achat.prix_total AS Prix,
    Client.nom_client AS Nom,
    Client.prenom_client AS Prenom
    FROM Achat
    JOIN Client ON Achat.id_client = Client.id_client;
    '''
    mycursor.execute(sql)
    achat = mycursor.fetchall()
    return render_template('achat/show_achat.html', achat=achat)


@app.route('/reduction/add', methods=['GET'])
def add_reduction():
    return render_template('reduction/add_reduction.html')


@app.route('/client/add', methods=['GET'])
def add_client():
    return render_template('client/add_client.html')


@app.route('/tri/add', methods=['GET'])
def add_tri():
    # Possible de rendre dynamique ? Dans les selectbox afficher que si possible selon contrainte unicité !
    mycursor = get_db().cursor()
    ramassage_sql = '''
    SELECT id_ramassage AS id, date_ramassage AS date
    FROM Ramassage
    ORDER BY date;
    '''
    vetement_sql = '''
    SELECT id_type AS id, libelle_type AS nom
    FROM Type_vetement
    ORDER BY nom;
    '''
    mycursor.execute(ramassage_sql)
    ramassages = mycursor.fetchall()
    mycursor.execute(vetement_sql)
    vetements = mycursor.fetchall()

    return render_template('tri/add_tri.html', ramassages=ramassages, vetements=vetements)


@app.route('/achat/add', methods=['GET'])
def add_achat():
    return render_template('achat/add_achat.html')


if __name__ == '__main__':
    app.run()
