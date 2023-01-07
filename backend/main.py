from flask import Flask,request, jsonify
from flask_cors import CORS
from xml.etree import ElementTree as ET
from gestor import Gestor

gestor = Gestor()

app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)

@app.route('/', methods=['GET'])
def prueba():
    return "Funcionando"

@app.route('/configuracion', methods=['POST'])
def agregar_configuracion():
    xml=request.data.decode('utf-8')
    raiz=ET.XML(xml)
    gestor.play_lists_client = []
    gestor.clientes = []
    gestor.empresas = []

    play_conteo = gestor.agregar_play_list(raiz.find("./playlistClientes"))
    cliente_conteo= gestor.agregar_clientes(raiz.find("./listaClientes"))
    empresa_conteo = gestor.agregar_empresa(raiz.find("./listaEmpresas"))
    return jsonify({"playConteo" : play_conteo, "clienteConteo":cliente_conteo, "empresaConteo": empresa_conteo})

@app.route('/consultarDatos', methods=['GET'])
def consultar_datos():
    return jsonify(gestor.mostrar_datos())

@app.route('/crearEmpresa', methods=['POST'])
def crear_empresa():
    xml=request.data.decode('utf-8')
    raiz=ET.XML(xml)
    gestor.agregar_empresa(raiz.find("./listaEmpresas"))
    return jsonify({"mensaje" : True})

@app.route('/crearPlaylist', methods=['POST'])
def crear_play_list():
    xml=request.data.decode('utf-8')
    raiz=ET.XML(xml)
    gestor.agregar_play_list(raiz.find("./playlistClientes"))
    return jsonify({"mensaje" : True})

@app.route('/crearCliente', methods=['POST'])
def crear_cliente():
    xml=request.data.decode('utf-8')
    raiz=ET.XML(xml)
    gestor.agregar_clientes(raiz.find("./listaClientes"))
    return jsonify({"mensaje" : True})

@app.route('/borrarCancion/<string:id>', methods=['DELETE'])
def eliminar_cancion(id):
    return jsonify({"mensaje":gestor.eliminar_cancion(id)})

@app.route('/borrarCliente/<string:nit>', methods=['DELETE'])
def eliminar_cliente(nit):
    return jsonify({"mensaje":gestor.eliminar_cliente(nit)})

@app.route('/factura/<string:id>', methods=['POST'])
def crear_factura(id):
    return jsonify(gestor.crear_factura(id))

if __name__ == '__main__':
    app.run(debug=True, port=4000)