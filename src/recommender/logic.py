import pandas as pd  # Biblioteca pentru manipularea datelor

def generate_recommendations(emotion, top_n=5):
    """
    Genereaza recomandari de filme bazate pe emotia primita.

    """    
    try:
        # Incarca datele din CSV
        df = pd.read_csv("data/movies_emotions.csv")
    except FileNotFoundError:
        print("Eroare: Fisierul CSV nu exista.")
        return []

    #  Filtreaza filmele cu emotia corespunzatoare
    filtered = df[df["emotion"].str.lower() == emotion.lower()]

    if filtered.empty:
        print(f"Nicio recomandare pentru emotia: {emotion}")
        return []

    # Sorteaza si selecteaza cele mai bune filme
    top_movies = filtered.sort_values(by="rating", ascending=False).head(top_n)
    
    return top_movies[["title", "genre", "description", "rating", "image"]].to_dict(orient="records")