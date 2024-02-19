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
    return jsonify({'error': 'Recurso no encontrado'}), 404

if __name__ == '__main__':
    load_dotenv()
    app.run()