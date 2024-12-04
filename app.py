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
    return redirect(url_for('abonneestable'))

@app.route('/delete_abonne', methods=['POST'])
def delete_abonne():
    email = request.form['email']
    result = db.abonne.delete_one({"email": email})

    if result.deleted_count == 0:
        return "Aucun abonné trouvé avec cet email.", 404

    return redirect(url_for('abonneestable'))

@app.route('/delete_all_abonnes', methods=['POST'])
def delete_all_abonnes():
    result = db.abonne.delete_many({})  # This deletes all documents in the collection

    if result.deleted_count == 0:
        return "Aucun abonné trouvé.", 404

    return redirect(url_for('abonneestable')) 

@app.route('/AbonneeEmails')
def abonnees_emails():
    emails = list(db.abonne.find({}, {"_id": 0, "email": 1}))  
    email_list = [email['email'] for email in emails]
    print("Emails récupérés :", email_list)  # Afficher dans la console
    return render_template('emprunt.html', emails=email_list)








@app.route('/update_abonne/<email>', methods=['POST'])
def update_abonne(email):
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    adresse = request.form.get('adresse')
    datedinscription = request.form.get('datedinscription')
    historiquedemprunts = request.form.get('historiquedemprunts')
    listedemprunts = request.form.get('listedemprunts')

    abonne = db.abonne.find_one({"email": email})
    
    if not abonne:
        return jsonify({"error": "Abonné introuvable"}), 404

    db.abonne.update_one(
        {"email": email},
        {"$set": {
            "nom": nom,
            "prenom": prenom,
            "adresse": adresse,
            "datedinscription": datedinscription ,
            "historiquedemprunts": historiquedemprunts,
            "listedemprunts": listedemprunts
        }}
    )

    return redirect(url_for('abonneestable'))


@app.route('/document', methods=['POST'])
def create_document():
    # Get form data from the request
    titre = request.form.get('titre')
    type_doc = request.form.get('type_doc')
    auteur = request.form.get('auteur')
    datedepublication = request.form.get('datedepublication')
    disponibilite = request.form.get('disponibilite')

    # Check if required fields are provided
    if not titre or not type_doc or not auteur:
        return jsonify({"error": "Titre, type_doc, and Auteur are required fields."}), 400

    # Validate and parse date if provided
    if datedepublication:
        try:
            datedepublication = datetime.strptime(datedepublication, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400

    # Prepare the data to insert into the database
    document_data = {
        "titre": titre,
        "type_doc": type_doc,
        "auteur": auteur,
        "datedepublication": datedepublication,
        "disponibilite": disponibilite
    }
    print(type_doc)  # Add this line to see what value is being received

    # Insert into the MongoDB collection
    db.document.insert_one(document_data)

    # Redirect to the document list or success page
    return redirect(url_for('documentstable'))


@app.route('/delete_document', methods=['POST'])
def delete_document():
    titre = request.form['titre']
    result = db.document.delete_one({"titre": titre})

    if result.deleted_count == 0:
        return "Aucun document trouvé avec cet titre.", 404

    return redirect(url_for('documentstable'))

@app.route('/delete_all_documents', methods=['POST'])
def delete_all_documents():
    result = db.document.delete_many({})  # This deletes all documents in the collection

    if result.deleted_count == 0:
        return "Aucun document trouvé.", 404

    return redirect(url_for('documentstable'))


@app.route('/update_document/<titre>', methods=['POST'])
def update_document(titre):
    type_doc = request.form.get('type_doc')
    auteur = request.form.get('auteur')
    datedepublication = request.form.get('datedepublication')
    disponibilite = request.form.get('disponibilite')

    document = db.document.find_one({"titre": titre})
    
    if not document:
        return jsonify({"error": "document introuvable"}), 404

    db.document.update_one(
        {"titre": titre},
        {"$set": {
        "type_doc": type_doc,
        "auteur": auteur,
        "datedepublication": datedepublication,
        "disponibilite": disponibilite
        }}
    )

    return redirect(url_for('documentstable'))


@app.route('/emprunt', methods=['POST'])
def create_emprunt():
    # Get form data from the request
    listeabonne = request.form.get('listeabonne')
    documentemprunté = request.form.get('documentemprunté')
    datedemprunt = request.form.get('datedemprunt')
    datederetourprévue = request.form.get('datederetourprévue')
    statutdelemprunt = request.form.get('statutdelemprunt')

    # Check if required fields are provided
    if not listeabonne or not documentemprunté or not datedemprunt:
        return jsonify({"error": "listeabonne, documentemprunté, and datedemprunt are required fields."}), 400

    # Validate and parse date if provided
    if datederetourprévue:
        try:
            datederetourprévue = datetime.strptime(datederetourprévue, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400

    if datedemprunt:
        try:
            datedemprunt = datetime.strptime(datedemprunt, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400

    # Prepare the data to insert into the database
    emprunt_data = {
        "listeabonne": listeabonne,
        "documentemprunté": documentemprunté,
        "datedemprunt": datedemprunt,
        "datederetourprévue": datederetourprévue,
        "statutdelemprunt": statutdelemprunt
    }


    # Insert into the MongoDB collection
    db.emprunt.insert_one(emprunt_data)

    # Redirect to the document list or success page
    return redirect(url_for('empruntstable'))


@app.route('/delete_emprunt', methods=['POST'])
def delete_emprunt():
    idEmprunt = request.form['idEmprunt']
    result = db.emprunt.delete_one({"idEmprunt": idEmprunt})

    if result.deleted_count == 0:
        return "Aucun emprunt trouvé avec cet idEmprunt.", 404

    return redirect(url_for('empruntstable'))

@app.route('/delete_all_emprunts', methods=['POST'])
def delete_all_emprunts():
    result = db.emprunt.delete_many({})  # This deletes all documents in the collection

    if result.deleted_count == 0:
        return "Aucun emprunt trouvé.", 404

    return redirect(url_for('empruntstable'))


@app.route('/update_emprunt/<idEmprunt>', methods=['POST'])
def update_emprunt(idEmprunt):
    listeabonne = request.form.get('listeabonne')
    documentemprunté = request.form.get('documentemprunté')
    datedemprunt = request.form.get('datedemprunt')
    datederetourprévue = request.form.get('datederetourprévue')
    statutdelemprunt = request.form.get('statutdelemprunt') 

    emprunt = db.emprunt.find_one({"idEmprunt": idEmprunt})
    
    if not emprunt:
        return jsonify({"error": "emprunt introuvable"}), 404

    db.emprunt.update_one(
        {"idEmprunt": idEmprunt},
        {"$set": {
        "listeabonne": listeabonne,
        "documentemprunté": documentemprunté,
        "datedempruntn": datedemprunt,
        "datederetourprévue": datederetourprévue,
        "statutdelemprunt":statutdelemprunt
        }}
    )

    return redirect(url_for('empruntstable'))
 




@app.route('/')
def home():
    total_abonnes = db.abonne.count_documents({}) 
    return render_template('index.html', total_abonnes=total_abonnes)


@app.route('/Shared')
def navbar():
    return render_template('shared.html')

@app.route('/AbonneeTable')
def abonneestable():
   abonnes = list(db.abonne.find({}, {"_id": 0})) 
   return render_template('abonnetable.html', abonnes=abonnes)

@app.route('/Abonnee')
def abonnees():
   abonnes = list(db.abonne.find({}, {"_id": 0})) 
   return render_template('abonne.html', abonnes=abonnes)

@app.route('/Document')
def documents():
   documents = list(db.document.find({}, {"_id": 0})) 
   return render_template('document.html', documents=documents)

@app.route('/DocumentTable')
def documentstable():
   documents = list(db.document.find({}, {"_id": 0})) 
   return render_template('documenttable.html', documents=documents)

@app.route('/Emprunt')
def emprunts():
   emprunts = list(db.emprunt.find({}, {"_id": 0})) 
   return render_template('emprunt.html', emprunts=emprunts)

@app.route('/EmpruntTable')
def empruntstable():
   emprunts = list(db.emprunt.find({}, {"_id": 0})) 
   return render_template('emprunttable.html', emprunts=emprunts)

if __name__ == "__main__":
    app.run(debug=True)



