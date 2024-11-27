from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]

# Blueprint pour les routes 'emprunt'
emprunt_bp = Blueprint('emprunt', __name__)

@emprunt_bp.route('/emprunt', methods=['POST'])
def create_emprunt():
    data = request.json
    db.emprunt.insert_one(data)
    return jsonify({"message": "Emprunt créé avec succès !"}), 201

@emprunt_bp.route('/emprunt', methods=['GET'])
def get_emprunts():
    emprunts = list(db.emprunt.find({}, {"_id": 0}))
    return jsonify(emprunts), 200

@emprunt_bp.route('/emprunt/<abonne>', methods=['PUT'])
def update_emprunt(abonne):
    data = request.json
    db.emprunt.update_one({"abonne": abonne}, {"$set": data})
    return jsonify({"message": "Emprunt mis à jour avec succès !"}), 200

@emprunt_bp.route('/emprunt/<abonne>', methods=['DELETE'])
def delete_emprunt(abonne):
    db.emprunt.delete_one({"abonne": abonne})
    return jsonify({"message": "Emprunt supprimé avec succès !"}), 200
