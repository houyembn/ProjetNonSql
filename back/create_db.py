from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Specify the database name
db_name = "gestionabonnee"
db = client[db_name]

# Create a collection and insert a sample document
db.abonne.insert_one({"nom": "Test", "prenom": "test", "adresse":"test@gmail.com", "datedinscription":"12-12-2001", "listedemprunts":"test", "historiquedemprunts":"test"})
db.document.insert_one({"titre": "Test", "type_doc": "test", "auteur":"test@gmail.com", "datedepublication":"12-12-2001", "disponibilite":"test"})
db.emprunt.insert_one({"abonne": "Test", "documentemprunte": "test","datedemprunt":"12-12-2001", "datederetour":"12-12-2001", "statusemprunt":"test"})
# db.emprunt.insert_one({"listeabonne": "Test", "documentemprunté": "test","datedemprunt":"12-12-2001", "datederetourprévue":"12-12-2001", "statutdelemprunt":"test"})

print(f"Database '{db_name}' created successfully with a sample document.")
