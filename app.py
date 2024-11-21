from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

@app.route('/reduction/show', methods=['GET'])
def show_reduction():
    return render_template('reduction/show_reduction.html')

if __name__ == '__main__':
    app.run()
