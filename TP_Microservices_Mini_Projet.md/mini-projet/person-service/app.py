import os
import datetime
import functools
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


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


@app.cli.command('create-db')
def create_db():
    """Create the database tables."""
    db.create_all()
    print('Database created')


@app.route('/persons', methods=['POST'])
@token_required
def create_person():
    data = request.get_json() or {}
    name = data.get('name')
    if not name or not isinstance(name, str):
        return jsonify({'error': 'name is required'}), 400

    p = Person(name=name)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route('/persons', methods=['GET'])
@token_required
def list_persons():
    persons = Person.query.order_by(Person.id.asc()).all()
    return jsonify([p.to_dict() for p in persons])


@app.route('/persons/search', methods=['GET'])
@token_required
def search_person():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({'error': 'name query param required'}), 400
    person = Person.query.filter(Person.name.ilike(name)).first()
    if not person:
        return jsonify({'error': 'not found'}), 404
    return jsonify(person.to_dict())


@app.route('/persons/<int:person_id>', methods=['GET'])
@token_required
def get_person(person_id):
    p = Person.query.get(person_id)
    if not p:
        return jsonify({'error': 'not found'}), 404
    return jsonify(p.to_dict())


@app.route('/persons/<int:person_id>', methods=['PUT'])
@token_required
def update_person(person_id):
    p = Person.query.get(person_id)
    if not p:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json() or {}
    name = data.get('name')
    if not name or not isinstance(name, str):
        return jsonify({'error': 'name is required'}), 400
    p.name = name
    db.session.commit()
    return jsonify(p.to_dict())


@app.route('/persons/<int:person_id>', methods=['DELETE'])
@token_required
def delete_person(person_id):
    p = Person.query.get(person_id)
    if not p:
        return jsonify({'error': 'not found'}), 404
    db.session.delete(p)
    db.session.commit()
    return '', 204


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    env_user = os.environ.get('AUTH_USER', 'admin')
    env_password = os.environ.get('AUTH_PASSWORD', 'password')

    if username != env_user or password != env_password:
        return jsonify({'error': 'invalid credentials'}), 401

    payload = {
        'sub': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    # PyJWT>=2.0 returns str, but ensure it's str in all cases
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({'access_token': token})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
