# redis_client.py - Client pentru interactiunea cu Redis (cache temporar)

import redis
import os

# Initializeaza conexiunea la Redis folosind URL
# sau la o instanta locala pe portul implicit (6379)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# Creeaza client Redis
r = redis.from_url(redis_url)

def save_last_emotion(username, emotion):
    """
    Salveaza ultima emotie detectata pentru un utilizator in Redis.
    
    """
    r.set(f"emotion:{username}", emotion)  # Seteaza pereche cheie-valoare

def get_last_emotion(username):
    """
    Returneaza ultima emotie salvata pentru un utilizator din Redis.
    
    """
    value = r.get(f"emotion:{username}")  # Obtine valoarea asociata cheii
    
    return value.decode("utf-8") if value else None