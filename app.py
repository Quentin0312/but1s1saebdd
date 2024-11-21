from flask import Flask, render_template

app = Flask(__name__)

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
