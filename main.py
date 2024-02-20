from flask import jsonify
from src import init_app
from dotenv import load_dotenv
from config import config

app = init_app(config['development'])


@app.route('/', methods=['GET'])
def index():
    return 'Bienvenido a la API de la tienda virtual'


@app.errorhandler(404)
def not_found(error):
    return jsonify({'succes': False, 'message': 'Recurso no encontrado'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'succes': False, 'message': 'Método no permitido'}), 405


@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'succes': False, 'message': 'Tipo de dato no soportado'}), 415


if __name__ == '__main__':
    load_dotenv()
    app.run()
