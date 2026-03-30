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
    # Ce print apparaîtra toujours dans tes logs terminal (kubectl logs)
    print("LOG: Visite détectée - Message pour MAROUA envoyé")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. On INSÈRE une nouvelle visite
        cur.execute("INSERT INTO visits (ts) VALUES (now());")
        conn.commit()
        
        # 2. On COMPTE le nombre total de visites
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        # 3. RETOUR HTML : Ce qui s'affiche sur la page web
        return f"""
        <html>
            <head>
                <title>DevOps Project - Master BD2C</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }}
                    .container {{ background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #2c3e50; }}
                    .count {{ font-size: 24px; color: #e74c3c; font-weight: bold; }}
                    .dedicace {{ color: #3498db; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Hello from Kubernetes! 🚀</h1>
                    <p>Félicitations, ton pipeline CI/CD fonctionne parfaitement.</p>
                    <p>Nombre total de visites enregistrées : <span class="count">{count}</span></p>
                    
                    <div class="dedicace">
                        <h2>Dédicace spéciale à MAROUA ! ✨</h2>
                        <p><i>Ceci est une mise à jour en direct via GitHub Actions.</i></p>
                    </div>
                </div>
            </body>
        </html>
        """
        
    except Exception as e:
        return f"<h1>Erreur de connexion DB</h1><p>{e}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)