# from flask import Flask

# # Initialisation de Flask
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Hello!"

# if __name__ == "__main__":
#     # Afficher "hello!" dans la console avant de démarrer l'application
#     print("hello!")
    
#     # Démarrage de l'application Flask
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__, static_folder='front/static', template_folder='front/templates')

client = MongoClient("mongodb://localhost:27017/")
db = client["gestionabonnee"]

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



