from flask import Flask, request, jsonify, Response
from recherche import recuperer_patient_par_id

app = Flask(__name__)

@app.route('/patient/recherche', methods=['POST'])
def search_patient():

    data = request.get_json()
    
 
    if not data or 'id' not in data:
        return jsonify({"erreur": "Veuillez fournir un champ 'id' dans le JSON"}), 400

    id_patient = data['id']


    resultat_string = recuperer_patient_par_id(int(id_patient))
    

    return Response(resultat_string, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5000)