import json
import os

chemin = "BDD102/data.json"

def recuperer_patient_par_id(id_recherche):

    
    # Vérifier si le fichier existe
    if not os.path.exists(chemin):
        return json.dumps({"erreur": "Fichier de base de données introuvable"})

    try:
        # Ouverture et lecture du fichier
        with open(chemin, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Parcours des patients pour trouver l'ID
        for patient in data:
            if patient['id'] == id_recherche:
                # On a trouvé le patient, on le convertit en JSON propre
                return json.dumps(patient, indent=4, ensure_ascii=False)
        
        # Si la boucle se termine sans trouver l'ID
        return json.dumps({"erreur": "Patient non trouvé"}, indent=4)

    except json.JSONDecodeError:
        return json.dumps({"erreur": "Le fichier JSON est mal formé"})

# --- Zone de test (Exécutée seulement si on lance ce fichier directement) ---
if __name__ == "__main__":
    print("--- Recherche de patient ---")
    try:
        # Demande à l'utilisateur d'entrer un ID
        saisie = input("Entrez l'ID du patient : ")
        id_a_chercher = int(saisie)
        
        # Appel de la fonction
        resultat = recuperer_patient_par_id(id_a_chercher)
        
        # Affichage du résultat
        print("\nRésultat de la recherche :")
        print(resultat)
        
    except ValueError:
        print("Erreur : Veuillez entrer un numéro valide pour l'ID.")