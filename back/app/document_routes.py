from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]

# Blueprint pour les routes 'document'
document_bp = Blueprint('document', __name__)

@document_bp.route('/document', methods=['POST'])
def create_document():
    data = request.json
    db.document.insert_one(data)
    return jsonify({"message": "Document créé avec succès !"}), 201

@document_bp.route('/document', methods=['GET'])
def get_documents():
    documents = list(db.document.find({}, {"_id": 0}))
    return jsonify(documents), 200

@document_bp.route('/document/<titre>', methods=['PUT'])
def update_document(titre):
    data = request.json
    db.document.update_one({"titre": titre}, {"$set": data})
    return jsonify({"message": "Document mis à jour avec succès !"}), 200

@document_bp.route('/document/<titre>', methods=['DELETE'])
def delete_document(titre):
    db.document.delete_one({"titre": titre})
    return jsonify({"message": "Document supprimé avec succès !"}), 200



from flask import request, jsonify, redirect, url_for
from datetime import datetime

@app.route('/document', methods=['POST'])
def create_document():

     # Get the JSON data from the request
    data = request.json

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
    if date_publication:
        try:
            date_publication = datetime.strptime(date_publication, '%Y-%m-%d')
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

    # Insert into the MongoDB collection
    db.document.insert_one(document_data)

    # Return a success message
    return jsonify({"message": "document créé avec succès !"}), 201

