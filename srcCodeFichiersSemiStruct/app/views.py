from flask import render_template, request, redirect, url_for, make_response
from app import models
from app import app
from app.models import Etudiant
import jwt
import datetime

import os

SECRET_KEY = app.config.get('SECRET_KEY', 'mysecretkey')
PASSWORD = os.environ.get('STUDENT_APP_PASSWORD', '1234')

@app.route('/')
def index():
    etudiants = models.get_etudiants()
    return render_template('index.html', etudiants=etudiants)

@app.route('/new')
def new_etudiant():
    return render_template('new.html')

@app.route('/auth', methods=['POST'])
def auth():
    nom = request.form['nom']
    addr = request.form['addr']
    pin = request.form['pin']
    password = request.form['password']
    if password != PASSWORD:
        return "Mot de passe incorrect", 403
    token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    models.ajouter_etudiant(nom, addr, pin)

    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', token)
    return resp

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_etudiant(id):
    if request.method == 'POST':
        addr = request.form['addr']
        pin = request.form['pin']
        models.update_etudiant(id, addr, pin)
        return redirect(url_for('index'))

    etudiant = Etudiant.query.get_or_404(id)
    return render_template('new.html', etudiant=etudiant)


# --- Minimal JSON API endpoints for Swagger ---
from flask import jsonify, request

@app.route('/api/students', methods=['GET','POST'])
def api_students():
    if request.method == 'GET':
        etuds = [e.to_dict() for e in models.get_etudiants()]
        return jsonify(etuds)
    data = request.get_json() or {}
    nom = data.get('nom')
    addr = data.get('addr')
    pin = data.get('pin')
    if not nom:
        return jsonify({'error': 'nom is required'}), 400
    try:
        models.ajouter_etudiant(nom, addr, pin)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'created'}), 201

@app.route('/api/students/<int:id>', methods=['GET','PUT'])
def api_student(id):
    if request.method == 'GET':
        e = Etudiant.query.get_or_404(id)
        return jsonify(e.to_dict())
    data = request.get_json() or {}
    addr = data.get('addr')
    pin = data.get('pin')
    models.update_etudiant(id, addr, pin)
    return jsonify({'message': 'updated'})

@app.route('/docs')
def docs():
    return render_template('docs.html')

if __name__ == "__main__":
    app.run(debug=True)
