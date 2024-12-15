from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for,jsonify
from datetime import datetime


app = Flask(__name__, static_folder='front/static', template_folder='front/templates')

client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]
abonnes_collection = db['abonne']

# Static credentials for additional login case
correct_email = "admin@example.com"
correct_password = "admin123"

@app.route('/abonne', methods=['POST'])
def create_abonne():
    # Get form data from the request
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    adresse = request.form.get('adresse')
    datedinscription = request.form.get('datedinscription')
    motdepasse = request.form.get('motdepasse')
    # historiquedemprunts = request.form.get('historiquedemprunts')
    # listedemprunts = request.form.get('listedemprunts')

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
        "motdepasse": motdepasse,
        # "historiquedemprunts": historiquedemprunts,
        # "listedemprunts": listedemprunts
    }

    # Insert into the MongoDB collection
    db.abonne.insert_one(abonne_data)
    
    # Return a success message
    return redirect(url_for('abonneestable'))



# @app.route('/emprunt', methods=['GET', 'POST'])
# def emprunt():
#     # Si la requête est GET, afficher le formulaire avec tous les abonnés
#     if request.method == 'GET':
#         abonnés = db.abonne.find()  # Requête MongoDB pour récupérer tous les abonnés
#         abonnés_list = list(abonnés)  # Convertir le curseur MongoDB en liste
#         return render_template('emprunt_form.html', abonnés=abonnés_list)

#     # Si la requête est POST, gérer la soumission du formulaire
#     if request.method == 'POST':
#         abonne = request.form.get('abonne')
#         document_emprunté = request.form.get('documentemprunté')
        
#         # Ajouter la logique pour traiter la soumission du formulaire (par exemple, créer un emprunt)
        
#         return redirect(url_for('success_page'))



@app.route('/delete_abonne', methods=['POST'])
def delete_abonne():
    email = request.form['email']
    result = db.abonne.delete_one({"email": email})

    if result.deleted_count == 0:
        return "Aucun abonné trouvé avec cet email.", 404

    return redirect(url_for('abonneestable'))

@app.route('/delete_all_abonnes', methods=['POST'])
def delete_all_abonnes():
    result = db.abonne.delete_many({})

    if result.deleted_count == 0:
        return "Aucun abonné trouvé.", 404

    return redirect(url_for('abonneestable')) 

@app.route('/AbonneeEmails')
def abonnees_emails():
    emails = list(db.abonne.find({}, {"_id": 0, "email": 1}))  
    email_list = [email['email'] for email in emails]
    print("Emails récupérés :", email_list)
    return render_template('emprunt.html', emails=email_list)








@app.route('/update_abonne/<email>', methods=['POST'])
def update_abonne(email):
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    adresse = request.form.get('adresse')
    datedinscription = request.form.get('datedinscription')
    motdepasse = request.form.get('motdepasse')
    # historiquedemprunts = request.form.get('historiquedemprunts')
    # listedemprunts = request.form.get('listedemprunts')

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
            "motdepasse": motdepasse,
            # "historiquedemprunts": historiquedemprunts,
            # "listedemprunts": listedemprunts
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


@app.route('/Emprunt')
def Emprunt():
    # Fetching emprunts, abonnés, and documents for listing
    emprunts = list(db.emprunt.find({}, {"_id": 0})) 
    # emprunts = list(db.emprunt.find({}, {"_id": 0, "datedemprunt": 1, "datederetour": 1, "documentemprunte": 1}))
    abonnes = list(db.abonne.find({}, {"_id": 0, "email": 1,}))
    documents = list(db.document.find({}, {"_id": 0, "titre": 1, "disponibilite": 1}))  # Include "disponibilite"
    
    # Debugging output
    print("Abonnés:", abonnes)
    print("Documents:", documents)
    
    return render_template('emprunt.html', emprunts=emprunts, abonnes=abonnes, documents=documents)


@app.route('/addemprunts', methods=['GET', 'POST'])
def addemprunts():
    if request.method == 'POST':
        # Collecting form data
        data = {
            "reference": request.form.get("reference"),
            "abonne": request.form.get("abonne"),
            "documentemprunte": request.form.get("documentemprunte"),
            "datedemprunt": request.form.get("datedemprunt"),
            "datederetour": request.form.get("datederetour"),
            "statusemprunt": request.form.get("statusemprunt")
        }
        
        # Inserting into the 'Emprunts' collection
        db.emprunt.insert_one(data)
        
        # Redirect to 'emprunts' route after successful insertion
        return redirect(url_for('empruntstable'))

    # Fetching abonnés and documents for the form
    # abonnes = list(db.abonne.find({}, {"_id": 0, "nom": 1, "prenom": 1}))
    abonnes = list(db.abonne.find({}, {"_id": 0, "email": 1}))

    documents = list(db.document.find({}, {"_id": 0, "titre": 1}))
    
    # Render 'emprunt.html' with data
    return render_template('emprunttable.html', abonnes=abonnes, documents=documents)

 
@app.route('/delete_emprunt', methods=['POST'])
def delete_emprunt():
    reference= request.form['reference']
    result = db.emprunt.delete_one({"reference": reference})

    if result.deleted_count == 0:
        return "Aucun emprunt trouvé avec cet reference.", 404

    return redirect(url_for('empruntstable'))

@app.route('/delete_all_emprunts', methods=['POST'])
def delete_all_emprunts():
    result = db.emprunt.delete_many({})  # This deletes all documents in the collection

    if result.deleted_count == 0:
        return "Aucun emprunt trouvé.", 404

    return redirect(url_for('empruntstable'))


@app.route('/update_emprunt/<reference>', methods=['POST'])
def update_emprunt(reference):
    abonne= request.form.get("abonne")
    documentemprunte=request.form.get("documentemprunte")
    datedemprunt= request.form.get("datedemprunt")
    datederetour= request.form.get("datederetour")
    statusemprunt= request.form.get("statusemprunt")

    emprunt = db.emprunt.find_one({"reference": reference})
    
    if not emprunt:
        return jsonify({"error": "emprunt introuvable"}), 404

    db.emprunt.update_one(
        {"reference": reference},
        {"$set": {
        "abonne":abonne,
        "documentemprunte":documentemprunte,
        "datedemprunt":datedemprunt,
        "datederetour":datederetour,
        "statusemprunt":statusemprunt
        }}
    )

    return redirect(url_for('empruntstable'))

    # Fetching abonnés and documents for the form
    abonnes = list(db.abonne.find({}, {"_id": 0, "email": 1,}))
    documents = list(db.document.find({}, {"_id": 0, "titre": 1}))
    
    # Render 'emprunt.html' with data
    return render_template('emprunttable.html', abonnes=abonnes, documents=documents)
 
import random

@app.route('/calendar-data')
def calendar_data():
    colors = ["#6C7EE1", "#92B9E3", "#FFC4A4", "#FBA2D0", "#C688EB", "#FD7238"]
    emprunts = list(db.emprunt.find({}, {"_id": 0, "datedemprunt": 1, "datederetour": 1, "documentemprunte": 1}))
    
    events = []
    for emprunt in emprunts:
        color = random.choice(colors)
        events.append({
            "title": emprunt["documentemprunte"],
            "start": emprunt["datedemprunt"],
            "end": emprunt["datederetour"],
            "color": color
        })

    return jsonify(events)



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         # Vérification des identifiants
#         if email == correct_email and password == correct_password:
#             return redirect(url_for('home'))  # Redirection vers la page d'accueil
#         else:
#             return render_template('login.html', error="Identifiants incorrects.")  # Afficher un message d'erreur

#     return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email matches static credentials
        if email == correct_email and password == correct_password:
            # Redirect to a static home page
            return redirect(url_for('home'))

        # Check if the abonné exists in MongoDB
        abonne = abonnes_collection.find_one({"email": email})

        if abonne and abonne['motdepasse'] == password:
            # Redirect to a personalized page for the abonné
            return redirect(url_for('abonne_home', email=email))

        # Invalid credentials
        return render_template('login.html', error="Identifiants incorrects.")

    return render_template('login.html')


@app.route('/abonne_home/<email>')
def abonne_home(email):
    # Fetch the abonné's data using their email
    abonne = abonnes_collection.find_one({"email": email})

    if not abonne:
        return "Abonné non trouvé.", 404  # Abonné not found

    # Fetch emprunts related to this abonné
    emprunts = list(db.emprunt.find({"abonne": email}))

    # Render the template with abonné and emprunt data
    return render_template('abonne_home.html', abonne=abonne, emprunts=emprunts)


@app.route('/home')
def home():
    total_abonnes = db.abonne.count_documents({})
    total_documents = db.document.count_documents({})
    total_emprunts = db.emprunt.count_documents({})
    return render_template('index.html', total_abonnes=total_abonnes, total_documents=total_documents,total_emprunts=total_emprunts)

@app.route('/Calender')
def Calender():
    return render_template('calender.html')

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


@app.route('/chart')
def chart():
    # Count total documents
    total_documents = db.document.count_documents({})
    
    # Retrieve all documents and extract the 'type_doc' field
    document_types = [doc.get('type_doc', 'Unknown') for doc in document.find()]
    
    # Count occurrences of each document type
    type_counts = Counter(document_types)
    
    # Calculate percentages
    percentages = {doc_type: (count / total_documents) * 100 for doc_type, count in type_counts.items()}
    
    # Prepare labels and values for the chart
    labels = list(percentages.keys())
    values = list(percentages.values())
    
    # Send data as JSON string to the template
    data = {
        'labels': labels,
        'values': values
    }
    
    return render_template('index.html', data=json.dumps(data))


@app.route('/chart_data')
def chart_data():
    # Example: Get the count of documents by type
    document_types = db.document.aggregate([
        {"$group": {"_id": "$type_doc", "count": {"$sum": 1}}}
    ])
    data = [{"type": doc["_id"], "count": doc["count"]} for doc in document_types]

    return jsonify(data)



@app.route('/api/loan_status_stats', methods=['GET'])
def get_loan_status_stats():
    try:
        # Regrouper les emprunts par statut et compter leur occurrence
        pipeline = [
            {"$group": {"_id": "$statusemprunt", "total": {"$sum": 1}}}
        ]
        loan_statuses = list(db.emprunt.aggregate(pipeline))
        
        # Préparer les données pour le front-end
        response_data = [{"status": doc["_id"], "count": doc["total"]} for doc in loan_statuses]
        
        return jsonify({"status": "success", "data": response_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)



