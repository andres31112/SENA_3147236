
from flask import Flask, render_template


app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def login():
    return render_template('inisio_sesion.html')

@app.route('/recueprar_contrasena')
def recuperar_contrasena():
    return render_template('recuperar_contrasena.html')

if __name__ == '__main__':
    app.run(debug=True)