from flask import Flask,jsonify,request
from flask_cors import CORS


app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)

nombre = {"Nombre":"Ruben", "Apellido":"Ralda","Carnet":202111835}

@app.route('/consultarDatos', methods=['GET'])
def consultar_datos():
    return jsonify(nombre)

if __name__ == '__main__':
    app.run(debug=True, port=4000)