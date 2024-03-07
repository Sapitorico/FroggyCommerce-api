from flask import jsonify
from src import init_app
from dotenv import load_dotenv
from config import config

# Initialize Flask application
app = init_app(config['development'])


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the virtual store API'


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Resource not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'message': 'Method not allowed'}), 405


@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'success': False, 'message': 'Unsupported media type'}), 415


if __name__ == '__main__':
    load_dotenv()
    app.run()
