from flask import Flask, request, render_template, redirect, flash, session, g, jsonify
import pymysql.cursors
# TODO : TO REMOVE !! -----------------------
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
username = os.getenv("MY_USERNAME")
mdp = os.getenv("MDP")
database = os.getenv("DATABASE")
print(username, mdp, database)
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
    mycursor = get_db().cursor()
    sql = '''
        SELECT Client.id_client AS id,
               Client.nom_client AS nomClient,
               Client.prenom_client AS prenomClient,
               Client.tel_client AS telClient,
               Client.adresse_client  AS adresseClient,
               Client.email_client AS emailClient,
               TIMESTAMPDIFF(YEAR, Client.date_naissace_client, CURRENT_DATE) AS ageClient,
               Cat.libelle_categorie AS nomCategorie
        FROM Client
        RIGHT JOIN Categorie_client Cat on Client.id_categorie = Cat.id_categorie
        HAVING id_client IS NOT NULL
        ORDER BY id_client;
        '''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('client/show_client.html', clients=clients)


@app.route('/tri/show', methods=['GET'])
def show_tri():
    mycursor = get_db().cursor()
    sql = '''
    SELECT Tri.id_tri AS id,
           R.date_ramassage AS dateRamassage,
           Tri.id_ramassage AS idRamassage,
           Tri.id_type      AS idTypeVetement,
           Tv.libelle_type  AS nomTypeVetement,
           poids_type_trie  AS quantite,
           ROUND(Tv.prix_kg_type * poids_type_trie,2) AS valeur
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
    Client.prenom_client AS Prenom,
    Client.id_client AS IdClient
    FROM Achat
    JOIN Client ON Achat.id_client = Client.id_client;
    '''
    mycursor.execute(sql)
    achat = mycursor.fetchall()
    return render_template('achat/show_achat.html', achat=achat)


@app.route('/achat/add', methods=['POST'])
def valid_add_achat():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    sql = " INSERT INTO Achat (libelle) VALUES (%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté, libellé : ' + libelle
    flash(message, 'alert-success')
    return redirect('/achat/show')


@app.route('/reduction/add', methods=['GET'])
def add_reduction():
    return render_template('reduction/add_reduction.html')


@app.route('/client/add', methods=['GET'])
def add_client():
    mycursor = get_db().cursor()
    sql = '''
        SELECT Categorie_client.id_categorie AS id, 
            Categorie_client.libelle_categorie AS nomCategorie
        FROM Categorie_client;
        '''
    mycursor.execute(sql)
    catClient = mycursor.fetchall()
    return render_template('client/add_client.html', catClient=catClient)


@app.route('/client/add', methods=['POST'])
def valid_add_client():
    nomClient = request.form.get('nomClient')
    prenomClient = request.form.get('prenomClient')
    telClient = request.form.get('telClient')
    adresseClient = request.form.get('adresseClient')
    emailClient = request.form.get('emailClient')
    dateClient = request.form.get('dateClient')
    dateClient = datetime.strptime(dateClient, '%Y-%m-%d').date()
    idCategorie = request.form.get('idCategorie')

    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Client (id_client, nom_client, prenom_client, tel_client, adresse_client, email_client,
                    date_naissace_client,
                    id_categorie) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);'''
    tuple_sql = (nomClient, prenomClient, telClient, adresseClient, emailClient, dateClient, idCategorie)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()

    return redirect('/client/show')


@app.route('/tri/add', methods=['GET'])
def add_tri():
    mycursor = get_db().cursor()
    # Récupère uniquement les ramassages dont il est encore possible d'ajouter un tri
    # TODO : Fix bug quand essaie d'ajouter alors que pas de tri !
    sql = '''
    SELECT sous_requete.id_ramassage AS id, Ramassage.date_ramassage AS date
    FROM (SELECT Ramassage.id_ramassage, COUNT(Tri.id_type) AS count
          FROM Ramassage
                   LEFT JOIN Tri ON Tri.id_ramassage = Ramassage.id_ramassage
          GROUP BY Ramassage.id_ramassage) AS sous_requete
             JOIN Ramassage ON Ramassage.id_ramassage = sous_requete.id_ramassage
    WHERE sous_requete.count < (SELECT COUNT(Type_vetement.id_type) FROM Type_vetement);
    '''
    mycursor.execute(sql)
    ramassages = mycursor.fetchall()

    if len(ramassages) == 0:
        # Rewrite the message
        flash(
            "Tout les types de vêtements sont traités dans tout les ramassages, pour ajouter un tri, veuillez d'abord un supprimer un !",
            'alert-danger')
        return redirect('/tri/show')

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

    mycursor = get_db().cursor()
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
    mycursor = get_db().cursor()
    sql = '''
    SELECT Client.id_client AS id, CONCAT(Client.nom_client, ' ', Client.prenom_client) AS nomClient
    FROM Client;
    '''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('achat/add_achat.html', clients=clients)


@app.route('/reduction/delete', methods=['GET'])
def delete_reduction():
    return redirect('/reduction/show')


@app.route('/client/delete', methods=['GET'])
def delete_client():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()

    sql = "SELECT id_achat AS id, date_achat AS dateAchat, prix_total AS prixAchat, id_client AS idClient FROM Achat WHERE id_client = %s;"
    mycursor.execute(sql, (id,))
    achats = mycursor.fetchall()

    if achats:
        return render_template('client/delete_client.html', achats=achats)

    else:
        sql = "DELETE FROM Client WHERE id_client = %s;"
        mycursor.execute(sql, (id,))
        get_db().commit()

        return redirect('/client/show')


@app.route('/client/fulldelete', methods=['GET'])
def fulldelete_client():
    id = request.args.get('id')
    idClient = request.args.get('idClient')
    mycursor = get_db().cursor()

    sql = "SELECT id_type, id_achat FROM Concerne WHERE id_achat = %s;"
    mycursor.execute(sql, (id,))
    concerne = mycursor.fetchall()

    if concerne:
        sql = "DELETE FROM Concerne WHERE id_achat = %s;"
        mycursor.execute(sql, (id,))
        get_db().commit()

    sql = "DELETE FROM Achat WHERE id_achat = %s;"
    mycursor.execute(sql, (id,))
    get_db().commit()

    sql = "SELECT id_achat AS id, date_achat AS dateAchat, prix_total AS prixAchat, id_client AS idClient FROM Achat WHERE id_client = %s;"
    mycursor.execute(sql, (idClient,))
    achats = mycursor.fetchall()

    if achats:
        return render_template('client/delete_client.html', achats=achats)

    else:
        sql = "DELETE FROM Client WHERE id_client = %s;"
        mycursor.execute(sql, (idClient,))
        get_db().commit()
        return redirect('/client/show')


@app.route('/tri/delete', methods=['GET'])
def delete_tri():
    id = request.args.get('id', '')

    mycursor = get_db().cursor()
    sql = "DELETE FROM Tri WHERE id_tri = %s;"
    mycursor.execute(sql, (id,))
    get_db().commit()

    return redirect('/tri/show')


@app.route('/achat/delete', methods=['GET'])
def delete_achat():
    return redirect('/achat/show')


@app.route('/reduction/edit', methods=['GET'])
def edit_reduction():
    return render_template('reduction/edit_reduction.html')


@app.route('/client/edit', methods=['GET'])
def edit_client():
    return render_template('client/edit_client.html')


@app.route('/tri/edit', methods=['GET'])
def edit_tri():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_tri                     AS id,
           Tri.id_type                AS idTypeVetement,
           Type_vetement.libelle_type AS nomTypeVetement,
           Tri.id_ramassage           AS idRamassage,
           Ramassage.date_ramassage   AS dateRamassage,
           poids_type_trie            AS quantite
    FROM Tri
             JOIN Type_vetement ON Tri.id_type = Type_vetement.id_type
             JOIN Ramassage ON Tri.id_ramassage = Ramassage.id_ramassage
    WHERE id_tri = %s;
    '''
    mycursor.execute(sql, (id,))
    tri = mycursor.fetchone()
    # TODO : Afficher message flash ?
    return render_template('tri/edit_tri.html', tri=tri)


@app.route('/tri/edit', methods=['POST'])
def valid_edit_tri():
    id = request.form['id']
    # idRamassage = request.form['ramassage_id']
    # idTypeVetement = request.form['typeVetement_id']
    quantite = request.form['quantite']

    mycursor = get_db().cursor()
    sql = '''
    UPDATE Tri SET poids_type_trie=%s WHERE id_tri=%s;
    '''
    mycursor.execute(sql, (quantite, id))
    get_db().commit()

    # Afficher message flash ?
    return redirect('/tri/show')


@app.route('/achat/edit', methods=['GET'])
def edit_achat():
    return render_template('achat/edit_achat.html')


@app.route('/reduction/etat', methods=['GET'])
def show_reduction_etat():
    return render_template('/reduction/etat_reduction.html')


@app.route('/client/etat', methods=['GET'])
def show_client_etat():
    return render_template('/client/etat_client.html')


@app.route('/tri/etat', methods=['GET'])
def show_tri_etat():
    # Bar chart
    mycursor = get_db().cursor()
    bar_chart_sql = '''
    SELECT Ramassage.date_ramassage AS dateRamassage, sous_requete.sum_poids_type_trie AS poidsTotal
    FROM (SELECT Tri.id_ramassage, SUM(Tri.poids_type_trie) AS sum_poids_type_trie
          FROM Tri
          GROUP BY Tri.id_ramassage) AS sous_requete
             JOIN Ramassage ON Ramassage.id_ramassage = sous_requete.id_ramassage
          ORDER BY Ramassage.date_ramassage;
    '''
    mycursor.execute(bar_chart_sql)
    barChartRaw = mycursor.fetchall()
    barChartLabels = [elt['dateRamassage'] for elt in barChartRaw]
    barChartLabels = [elt.strftime("%Y-%m-%d") for elt in barChartLabels]
    barChartData = [elt['poidsTotal'] for elt in barChartRaw]
    barChartData = [str(elt) for elt in barChartData]

    # Pie chart
    pie_chart_sql = '''
    SELECT Type_vetement.libelle_type AS typeVetement, sous_requete.sum_poids_type_trie AS poidsTotal
    FROM (SELECT Tri.id_type, SUM(Tri.poids_type_trie) AS sum_poids_type_trie
          FROM Tri
          GROUP BY Tri.id_type) AS sous_requete
             JOIN Type_vetement ON Type_vetement.id_type = sous_requete.id_type ORDER BY poidsTotal DESC;
    '''
    mycursor.execute(pie_chart_sql)
    pieChartRaw = mycursor.fetchall()
    pieChartLabels = [elt['typeVetement'] for elt in pieChartRaw]
    pieChartData = [str(elt['poidsTotal']) for elt in pieChartRaw]

    # Radar chart
    radar_chart_labels_sql = '''
    SELECT libelle_type AS label
    FROM Type_vetement
    ORDER BY id_type;
    '''
    mycursor.execute(radar_chart_labels_sql)
    radarChartLabelsRaw = mycursor.fetchall()
    radarChartLabels = [elt['label'] for elt in radarChartLabelsRaw]

    radar_chart_dataset_sql = '''
    SELECT Tri.id_type, Type_vetement.libelle_type, Tri.id_ramassage, Ramassage.date_ramassage, Tri.poids_type_trie
    FROM Tri
             JOIN Type_vetement ON Type_vetement.id_type = Tri.id_type
             JOIN Ramassage ON Ramassage.id_ramassage = Tri.id_ramassage
    ORDER BY Tri.id_ramassage, id_type;
    '''
    mycursor.execute(radar_chart_dataset_sql)
    radarChartDatasetRaw = mycursor.fetchall()
    radarChartData = {}

    for elt in radarChartDatasetRaw:
        elt_date_ramassage = elt['date_ramassage'].strftime("%Y-%m-%d")

        if elt_date_ramassage not in radarChartData.keys():
            radarChartData[elt_date_ramassage] = [0 for elt in radarChartLabels]

        radarChartData[elt_date_ramassage][elt['id_type'] - 1] = float(
            elt['poids_type_trie'])

    # Filter
    date_debut_pie_chart_sql = '''
    SELECT Ramassage.date_ramassage
    FROM Ramassage
    ORDER BY date_ramassage
    LIMIT 1;
    '''

    date_fin_pie_chart_sql = '''
    SELECT Ramassage.date_ramassage
    FROM Ramassage
    ORDER BY date_ramassage DESC
    LIMIT 1;
    '''

    mycursor.execute(date_debut_pie_chart_sql)
    dateDebutResponse = mycursor.fetchone()
    dateDebut = dateDebutResponse['date_ramassage'].strftime("%Y-%m-%d")

    mycursor.execute(date_fin_pie_chart_sql)
    dateFinResponse = mycursor.fetchone()
    dateFin = dateFinResponse['date_ramassage'].strftime("%Y-%m-%d")

    return render_template('/tri/etat_tri.html', barChartLabels=barChartLabels, barChartData=barChartData,
                           pieChartLabels=pieChartLabels, pieChartData=pieChartData, dateDebut=dateDebut,
                           dateFin=dateFin, radarChartLabels=radarChartLabels, radarChartData=radarChartData)


@app.route('/tri/etat/piechart', methods=['GET'])
def get_piechart_filtered_data():
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    mycursor = get_db().cursor()
    sql = ''' SELECT Type_vetement.libelle_type AS typeVetement, sous_requete.sum_poids_type_trie AS poidsTotal
    FROM (SELECT Tri.id_type, SUM(Tri.poids_type_trie) AS sum_poids_type_trie
          FROM Tri
                   JOIN Ramassage ON Ramassage.id_ramassage = Tri.id_ramassage
          WHERE date_ramassage BETWEEN %s AND %s
          GROUP BY Tri.id_type) AS sous_requete
             JOIN Type_vetement ON Type_vetement.id_type = sous_requete.id_type
    ORDER BY poidsTotal DESC;
    '''
    mycursor.execute(sql, (date_debut, date_fin))
    pieChartRaw = mycursor.fetchall()
    pieChartLabels = [elt['typeVetement'] for elt in pieChartRaw]
    pieChartData = [str(elt['poidsTotal']) for elt in pieChartRaw]
    result = jsonify({
        "labels": pieChartLabels,
        "data": pieChartData
    })
    return result

@app.route('/tri/etat/barchart', methods=['GET'])
def get_barchart_filtered_data():
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    mycursor = get_db().cursor()
    sql = '''
    SELECT Ramassage.date_ramassage AS dateRamassage, sous_requete.sum_poids_type_trie AS poidsTotal
    FROM (SELECT Tri.id_ramassage, SUM(Tri.poids_type_trie) AS sum_poids_type_trie
          FROM Tri
          GROUP BY Tri.id_ramassage) AS sous_requete
             JOIN Ramassage ON Ramassage.id_ramassage = sous_requete.id_ramassage
          WHERE date_ramassage BETWEEN %s AND %s
          ORDER BY Ramassage.date_ramassage;
    '''
    mycursor.execute(sql, (date_debut, date_fin))
    barChartRaw = mycursor.fetchall()
    barChartLabels = [elt['dateRamassage'] for elt in barChartRaw]
    barChartLabels = [elt.strftime("%Y-%m-%d") for elt in barChartLabels]
    barChartData = [elt['poidsTotal'] for elt in barChartRaw]
    barChartData = [str(elt) for elt in barChartData]

    result = jsonify({
        "labels": barChartLabels,
        "data": barChartData
    })
    return result

@app.route('/tri/etat/radarchart', methods=['GET'])
def get_radarchart_filtered_data():
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    mycursor = get_db().cursor()
    # Labels
    radar_chart_labels_sql = '''
    SELECT libelle_type AS label
    FROM Type_vetement
    ORDER BY id_type;
    '''
    mycursor.execute(radar_chart_labels_sql)
    radarChartLabelsRaw = mycursor.fetchall()
    radarChartLabels = [elt['label'] for elt in radarChartLabelsRaw]

    # Chart dataset
    sql = '''
    SELECT Tri.id_type, Type_vetement.libelle_type, Tri.id_ramassage, Ramassage.date_ramassage, Tri.poids_type_trie
    FROM Tri
             JOIN Type_vetement ON Type_vetement.id_type = Tri.id_type
             JOIN Ramassage ON Ramassage.id_ramassage = Tri.id_ramassage
    WHERE date_ramassage BETWEEN %s AND %s
    ORDER BY Tri.id_ramassage, id_type;
    '''
    mycursor.execute(sql, (date_debut, date_fin))
    radarChartRaw = mycursor.fetchall()
    radarChartData = {}

    for elt in radarChartRaw:
        elt_date_ramassage = elt['date_ramassage'].strftime("%Y-%m-%d")

        if elt_date_ramassage not in radarChartData.keys():
            radarChartData[elt_date_ramassage] = [0 for elt in radarChartLabels]

        radarChartData[elt_date_ramassage][elt['id_type'] - 1] = float(
            elt['poids_type_trie'])

    result = jsonify({
        "labels": radarChartLabels,
        "data": radarChartData
    })

    return result


@app.route('/achat/etat', methods=['GET'])
def show_achat_etat():
    return render_template('/achat/etat_achat.html')


if __name__ == '__main__':
    app.run()
