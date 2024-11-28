from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for,jsonify
from datetime import datetime


app = Flask(__name__, static_folder='front/static', template_folder='front/templates')

client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]

@app.route('/abonne', methods=['POST'])
def create_abonne():
    # Get form data from the request
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    adresse = request.form.get('adresse')
    datedinscription = request.form.get('datedinscription')
    historiquedemprunts = request.form.get('historiquedemprunts')
    listedemprunts = request.form.get('listedemprunts')

    # Check if required fields are provided
    if not nom or not prenom or not email:
        return jsonify({"error": "Nom, prénom, and email are required fields."}), 400

    # If 'datedinscription' is provided, ensure it's a valid date
    if datedinscription:
        try:
            datedinscription = datetime.strptime(datedinscription, '%Y-%m-%d')  # Directly parse the standard date format
        except ValueError:
            return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400

    # Prepare the data to insert into the database
    abonne_data = {
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "adresse": adresse,
        "datedinscription": datedinscription,
        "historiquedemprunts": historiquedemprunts,
        "listedemprunts": listedemprunts
    }

    # Insert into the MongoDB collection
    db.abonne.insert_one(abonne_data)
    
    # Return a success message
    return redirect(url_for('abonnees'))

    @app.route('/abonne/<email>', methods=['DELETE'])
    def delete_abonne(email):
     db.abonne.delete_one({"email": email})
     return jsonify({"message": "Abonné supprimé avec succès !"}), 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Shared')
def navbar():
    return render_template('shared.html')

@app.route('/Abonnee')
def abonnees():
   abonnes = list(db.abonne.find({}, {"_id": 0})) 
   return render_template('abonne.html', abonnes=abonnes)

if __name__ == "__main__":
    app.run(debug=True)


