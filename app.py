from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Configuration de la connexion (Utilise les variables d'environnement ou les valeurs par défaut)
DB_HOST = os.environ.get('DB_HOST', 'postgres-service')
DB_NAME = os.environ.get('DB_NAME', 'devopsdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'mypassword')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. On INSÈRE une nouvelle visite
        cur.execute("INSERT INTO visits (ts) VALUES (now());")
        conn.commit() # Très important pour sauvegarder l'insertion !
        
        # 2. On COMPTE le nombre total de visites pour l'afficher
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return f"Hello from Kubernetes! Nombre total de visites enregistrées : {count}"
        
    except Exception as e:
        return f"Erreur de connexion DB : {e}"
print("MAROUA HA HA HA HA HA HA HA HA ")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
