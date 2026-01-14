import json

chemin = "BDD101/data.json"

try:
    with open(chemin, 'r') as f:
        data = json.load(f)
    
    print("Lecture réussie !")
    print("Anciennes coordonnées :", data['features'][0]['geometry']['coordinates'])

    nouvelles_coords = [48.83, ] 
    data['features'][0]['geometry']['coordinates'] = nouvelles_coords
    print("Nouvelles coordonnées appliquées.")

    data['features'][0]['properties']['prop45'] = True
    
    print("Propriété 'prop45' ajoutée.")

    with open(chemin, 'w') as f:
        json.dump(data, f, indent=4)
    
    print("\nTout est sauvegardé dans data.json !")

except FileNotFoundError:
    print(f"Erreur : Le fichier est introuvable au chemin '{chemin}'. Vérifie l'emplacement.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")