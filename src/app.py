# Importuri necesare pentru aplicatia Flask
from flask import Flask, render_template, request, redirect, session, url_for
from db.mongodb_client import users_collection, save_recommendation, get_user_recommendations
from db.redis_client import save_last_emotion, get_last_emotion
from emotion_detector import detect_emotion
from recommender.logic import generate_recommendations
from aws.s3_upload import upload_recommendation
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "secretkey123")

# Ruta pentru pagina de start
@app.route('/')
def landing():
    """Afiseaza pagina de landing """
    return render_template('landing.html')

# Ruta pentru pagina principala
@app.route('/home')
def index():
    """
    Afiseaza pagina home doar daca utilizatorul este autentificat.
    Daca nu este logat, se redirectioneaza la pagina de login.
    """
    if 'username' not in session:  # Verifica daca exista username in sesiune
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Ruta pentru login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestioneaza procesul de autentificare:
    - GET: Afiseaza formularul de login
    - POST: Proceseaza datele de autentificare
    """
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        # Cauta utilizatorul in baza de date
        user = users_collection.find_one({'username': name})
        # Verifica daca utilizatorul exista si parola este corecta
        if user and check_password_hash(user['password'], password):
            session['username'] = name  # Seteaza username in sesiune
            return redirect(url_for('index'))  # Redirectioneaza la home
        # Daca autentificarea esueaza, afiseaza mesaj de eroare
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Ruta pentru inregistrare 
@app.route('/register', methods=['GET', 'POST'])
def register():
   
    if request.method == 'POST':
        # Genereaza hash pentru parola inainte de stocare
        hashed_pw = generate_password_hash(request.form['password'])
        # Salveaza noul utilizator in baza de date
        users_collection.insert_one({
            'username': request.form['username'],
            'password': hashed_pw
        })
        return redirect(url_for('login'))  # Redirectioneaza la login dupa inregistrare
    return render_template('register.html')

# Ruta pentru generare recomandari 
@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Proceseaza cererea de recomandari:
    1. Verifica daca utilizatorul este logat
    2. Detecteaza emotia din textul introdus
    3. Salveaza emotia in Redis
    4. Genereaza recomandari pe baza emotiei
    5. Salveaza recomandarile in MongoDB 
    6. Afiseaza rezultatele
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session["username"]
    feeling = request.form["feeling"]

    # Detecteaza emotia 
    emotion = detect_emotion(feeling)  

    # Salveaza ultima emotie in Redis pentru acces rapid
    save_last_emotion(username, emotion)

    # Genereaza recomandari pe baza emotiei detectate
    recommendations = generate_recommendations(emotion)

    # Incarca recomandarile in AWS S3
    # upload_recommendation(username, emotion, recommendations)

    # Salveaza recomandarile in MongoDB pentru istoric
    save_recommendation(username, emotion, recommendations)

    # Afiseaza pagina cu rezultatele
    return render_template("results.html", emotion=emotion, recommendations=recommendations)

# Ruta pentru profilul utilizatorului
@app.route('/profile')
def profile():
    """
    Afiseaza profilul utilizatorului cu:
    - Ultima emotie detectata (din Redis)
    - Istoricul recomandarilor (din MongoDB)
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    # Obtine ultima emotie din Redis
    emotion = get_last_emotion(username)
    # Obtine ultimele recomandari din MongoDB (limitate la 1 rezultat)
    past_recommendations = get_user_recommendations(username, limit=1)
    return render_template('profile.html', emotion=emotion, past_recommendations=past_recommendations)

# Ruta pentru delogare  
@app.route('/logout')
def logout():
    """
    Sterge toate datele din sesiune si redirectioneaza la pagina de start
    """
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)