# mongodb_client.py - Client pentru interactiunea cu baza de date MongoDB

from pymongo import MongoClient
import os

# Initializeaza conexiunea la serverul MongoDB
# Foloseste URI din variabila de mediu sau localhost pe portul implicit 
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))

# Selecteaza baza de date 'emotion_recommender'
db = client["emotion_recommender"]

# Defineste colectiile folosite in aplicatie
users_collection = db["users"]  # Colectie pentru stocarea utilizatorilor
recommendations_collection = db["recommendations"]  # Colectie pentru istoricul recomandarilor

def save_recommendation(username, emotion, recommendations):
    """
    Salveaza o recomandare in baza de date
    
    Args:
        username (str): Numele utilizatorului
        emotion (str): Emotia detectata
        recommendations (list): Lista de recomandari generate
    """
    recommendations_collection.insert_one({
        "username": username,  # Numele utilizatorului asociat
        "emotion": emotion,    # Emotia pe baza careia s-au generat recomandarile
        "recommendations": recommendations  # Lista de recomandari
    })

def get_user_recommendations(username, limit=5):
    """
    Returneaza ultimele recomandari pentru un utilizator
    
    Args:
        username (str): Numele utilizatorului
        limit (int): Numarul maxim de recomandari de returnat (implicit 5)
    
    Returns:
        list: Lista de documente cu recomandari, ordonate de la cele mai recente
    """
    return list(
        recommendations_collection
        .find({"username": username})  # Cauta doar recomandarile pentru acest utilizator
        .sort("_id", -1)  # Sorteaza descrescator dupa ID (cele mai recente prima)
        .limit(limit)     # Limiteaza numarul de rezultate returnate
    )