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
    return render_template('achat/show_achat.html')


@app.route('/reduction/add', methods=['GET'])
def add_reduction():
    return render_template('reduction/add_reduction.html')


@app.route('/client/add', methods=['GET'])
def add_client():
    return render_template('client/add_client.html')


@app.route('/tri/add', methods=['GET'])
def add_tri():
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_ramassage AS id, date_ramassage AS date
    FROM Ramassage
    ORDER BY date;
    '''

    mycursor.execute(sql)
    ramassages = mycursor.fetchall()

    return render_template('tri/add_tri.html', ramassages=ramassages)


@app.route('/tri/add', methods=['POST'])
def valid_add_tri():
    id_ramassage = request.form['ramassage_id']
    id_type = request.form['vetement_id']
    poids = request.form['quantite']

    mycursor = get_db().cursor()
    sql = '''
    INSERT INTO Tri (id_tri, id_type, id_ramassage, poids_type_trie)
    VALUES (NULL, %s, %s, %s);
    '''
    mycursor.execute(sql, (id_type, id_ramassage, poids,))
    get_db().commit()
    # TODO : Afficher message flash
    return redirect('/tri/show')


@app.route('/tri/add/vetement', methods=['GET'])
def show_type_vetement():
    idRamassage = request.args.get('id', '')

    mycursor = get_db().cursor();
    sql = '''
    SELECT Type_vetement.id_type AS id, Type_vetement.libelle_type AS nom
    FROM (SELECT Tri.id_tri, Tri.id_type
          FROM Tri
          WHERE Tri.id_ramassage = %s) as sousrequete
             RIGHT JOIN Type_vetement ON sousrequete.id_type = Type_vetement.id_type
    WHERE sousrequete.id_tri IS NULL;
    '''
    mycursor.execute(sql, (idRamassage,))
    vetements = mycursor.fetchall()

    return render_template("tri/_type_vetement.html", vetements=vetements)


@app.route('/achat/add', methods=['GET'])
def add_achat():
    return render_template('achat/add_achat.html')


if __name__ == '__main__':
    app.run()
