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
