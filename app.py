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
    sql = "SELECT * FROM Tri;"
    mycursor.execute(sql)
    tris = mycursor.fetchall()
    print(tris)
    return render_template('tri/show_tri.html')


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
    return render_template('tri/add_tri.html')


@app.route('/achat/add', methods=['GET'])
def add_achat():
    return render_template('achat/add_achat.html')


if __name__ == '__main__':
    app.run()
