
import os
import json
import functools
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import jwt
import requests

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
PERSON_SERVICE_URL = os.environ.get('PERSON_SERVICE_URL', 'http://person-service:5001')
DATA_FILE = os.environ.get('DATA_FILE', 'data.json')


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def token_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'authorization required'}), 401
        token = auth.split(' ', 1)[1]
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception:
            return jsonify({'error': 'invalid token'}), 401
        return f(*args, **kwargs)
    return wrapper


def person_exists(person_id, auth_header=None):
    try:
        headers = {'Authorization': auth_header} if auth_header else {}
        r = requests.get(f"{PERSON_SERVICE_URL}/persons/{person_id}", headers=headers, timeout=3)
        return r.status_code == 200
    except requests.RequestException:
        return False


@app.cli.command('init-data')
def init_data():
    """Create empty data file if missing."""
    if not os.path.exists(DATA_FILE):
        save_data({})
        print(f'Created empty {DATA_FILE}')
    else:
        print(f'{DATA_FILE} already exists')


def fetch_persons(auth_header):
    headers = {'Authorization': auth_header} if auth_header else {}
    r = requests.get(f"{PERSON_SERVICE_URL}/persons", headers=headers, timeout=3)
    if r.status_code != 200:
        return None
    return r.json()


@app.route('/health/<int:person_id>', methods=['GET'])
@token_required
def get_health(person_id):
    auth_header = request.headers.get('Authorization')
    if not person_exists(person_id, auth_header):
        return jsonify({'error': 'person not found'}), 404
    data = load_data()
    entry = data.get(str(person_id))
    if not entry:
        return jsonify({'error': 'no health data'}), 404
    return jsonify(entry)


@app.route('/health/<int:person_id>', methods=['POST'])
@token_required
def post_health(person_id):
    auth_header = request.headers.get('Authorization')
    if not person_exists(person_id, auth_header):
        return jsonify({'error': 'person not found'}), 404
    payload = request.get_json() or {}
    if not payload:
        return jsonify({'error': 'json body required'}), 400
    data = load_data()
    data[str(person_id)] = payload
    save_data(data)
    return jsonify(payload), 201


@app.route('/health/<int:person_id>', methods=['PUT'])
@token_required
def put_health(person_id):
    auth_header = request.headers.get('Authorization')
    if not person_exists(person_id, auth_header):
        return jsonify({'error': 'person not found'}), 404
    payload = request.get_json() or {}
    if not payload:
        return jsonify({'error': 'json body required'}), 400
    data = load_data()
    data[str(person_id)] = payload
    save_data(data)
    return jsonify(payload)


@app.route('/health/<int:person_id>', methods=['DELETE'])
@token_required
def delete_health(person_id):
    auth_header = request.headers.get('Authorization')
    if not person_exists(person_id, auth_header):
        return jsonify({'error': 'person not found'}), 404
    data = load_data()
    if str(person_id) in data:
        del data[str(person_id)]
        save_data(data)
    return '', 204


@app.route('/health/all', methods=['GET'])
@token_required
def list_health():
    auth_header = request.headers.get('Authorization')
    persons = fetch_persons(auth_header)
    if persons is None:
        return jsonify({'error': 'unable to fetch persons'}), 502
    data = load_data()
    combined = []
    for p in persons:
        pid = str(p.get('id'))
        combined.append({
            'id': p.get('id'),
            'name': p.get('name'),
            'health': data.get(pid) or {}
        })
    return jsonify(combined)
@app.route('/', methods=['GET'])
def index():
    template_path = os.path.join(os.path.dirname(__file__), 'template', 'index.html')
    return send_file(template_path, mimetype='text/html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
