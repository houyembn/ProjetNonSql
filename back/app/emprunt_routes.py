from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]

# Blueprint pour les routes 'emprunt'
emprunt_bp = Blueprint('emprunt', __name__)

# @emprunt_bp.route('/emprunt', methods=['POST'])
# def create_emprunt():
#     data = request.json
#     db.emprunt.insert_one(data)
#     return jsonify({"message": "Emprunt créé avec succès !"}), 201

@emprunt_bp.route('/emprunt', methods=['GET'])
def get_emprunts():
    emprunts = list(db.emprunt.find({}, {"_id": 0}))
    return jsonify(emprunts), 200

@emprunt_bp.route('/emprunt/<idEmprunt>', methods=['PUT'])
def update_emprunt(idEmprunt):
    data = request.json
    db.emprunt.update_one({"idEmprunt": idEmprunt}, {"$set": data})
    return jsonify({"message": "Emprunt mis à jour avec succès !"}), 200

@emprunt_bp.route('/emprunt/<idEmprunt>', methods=['DELETE'])
def delete_emprunt(idEmprunt):
    db.emprunt.delete_one({"idEmprunt": idEmprunt})
    return jsonify({"message": "Emprunt supprimé avec succès !"}), 200

# @app.route('/emprunt', methods=['POST'])
# def create_emprunt():

#      # Get the JSON data from the request
#     data = request.json

#     # Get form data from the request
#     listeabonne = request.form.get('listeabonne')
#     documentemprunté = request.form.get('documentemprunté')
#     datedemprunt = request.form.get('datedemprunt')
#     datederetourprévue = request.form.get('datederetourprévue')
#     statutdelemprunt = request.form.get('statutdelemprunt') 

#     # Check if required fields are provided
#     if not listeabonne or not documentemprunté or not datedemprunt:
#         return jsonify({"error": "listeabonne, documentemprunté, and datedemprunt are required fields."}), 400

#     # Validate and parse date if provided
#     if datederetourprévue:
#         try:
#             datederetourprévue = datetime.strptime(datederetourprévue, '%Y-%m-%d')
#         except ValueError:
#             return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400

#     if datedemprunt:
#         try:
#             datedemprunt = datetime.strptime(datedemprunt, '%Y-%m-%d')
#         except ValueError:
#             return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD."}), 400


#      emprunt_data = {
#         "listeabonne": listeabonne,
#         "documentemprunté": documentemprunté,
#         "datedemprunt": datedemprunt,
#         "datederetourprévue": datederetourprévue,
#         "statutdelemprunt": statutdelemprunt
#     }


#     # Insert into the MongoDB collection
#     db.emprunt.insert_one(emprunt_data)


#     # Return a success message
#     return jsonify({"message": "emprunt créé avec succès !"}), 201
