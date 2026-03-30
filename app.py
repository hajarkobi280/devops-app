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
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Hello from Kubernetes! Connected to: {db_version[0]}"
    except Exception as e:
        return f"Hello from Kubernetes! (But DB connection failed: {e})"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
