from app import app
from flask import render_template, request, jsonify

### EXO1 - simple API
@app.route('/api/salutation', methods=['GET'])
def salutation():
    return jsonify({"message": "Salut"})

### EXO2 - API with simple display
@app.route('/simple-html')
def simple_display():
    return "<h1>HTML simple </h1><p>Par El_Flaco27</p>"

### EXO3 - API with parameters display 
@app.route('/<name>')
def nom_perso(name):
    return f"<h1>Bonjour {name} !</h1><p>Ce paramètre vient de la route URL.</p>"

### EXO4 - API with parameters retrieved from URL 
@app.route('/recherche')
def recherche_url():
    terme_recupere = request.args.get('term', 'Inconnu')
    return render_template('search.html', le_terme=terme_recupere)