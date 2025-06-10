# emotion_detector.py - Sistem de detectare a emotiilor din text folosind NLP

from transformers import pipeline

# Foloseste un model BERT antrenat pentru clasificarea emotiilor
emotion_classifier = pipeline(
    'text-classification',  # Tipul de sarcina 
    model='nateraw/bert-base-uncased-emotion' 
)

def detect_emotion(text):
    """
    Detecteaza emotia predominanta dintr-un text.
    
    """
    # Analiza textului cu modelul NLP
    result = emotion_classifier(text)
    
    # Extrage eticheta principala 
    return result[0]['label'].lower()