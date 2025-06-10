# s3_upload.py - Modul pentru incarcare recomandari in AWS S3

import boto3
import json
import os
from dotenv import load_dotenv

# Incarca variabilele de mediu din fisierul .env
load_dotenv()

# Creeaza o sesiune AWS folosind credentialele din variabilele de mediu
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),       
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 
    region_name=os.getenv("AWS_REGION")                    
)

# Initializeaza clientul S3
s3 = session.client('s3')
# Obtine numele bucket-ului S3 din variabilele de mediu
BUCKET = os.getenv("S3_BUCKET_NAME")

def upload_recommendation(username, emotion, recommendations):
    """
    Incarca recomandarile generate in AWS S3 sub forma de fisier JSON.
    
    """
    # Genereaza nume de fisier unic pentru fiecare utilizator
    filename = f"{username}_recommendation.json"
    
    # Structureaza datele pentru salvare
    data = {
        "user": username,
        "emotion": emotion,
        "movies": recommendations
    }
    
    # Incarca fisierul JSON in bucket-ul S3
    s3.put_object(
        Bucket=BUCKET,                      # Numele bucket-ului
        Key=filename,                       # Numele fisierului in S3
        Body=json.dumps(data),              # Continutul JSON
        ContentType='application/json'     
    )