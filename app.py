from flask import Flask, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Configuration
DB_HOST = os.environ.get('DB_HOST', 'postgres-service')
DB_NAME = os.environ.get('DB_NAME', 'devopsdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'mypassword')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/')
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (ts) VALUES (now());")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial; text-align: center; background-color: #f4f4f9; padding: 50px; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }}
                h1 {{ color: #2c3e50; }}
                .count {{ font-size: 24px; color: #e74c3c; font-weight: bold; }}
                .blue {{ color: #3498db; border-top: 1px solid #eee; padding-top: 10px; }}
                .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Hello from Kubernetes! 🚀</h1>
                <p>Visites enregistrées : <span class="count">{count}</span></p>
                <div class="blue">
                    <h2>Dédicace spéciale à MAROUA ! ✨</h2>
                </div>
                <a href="/guestbook" class="btn">Aller au Livre d'Or 📖</a>
            </div>
        </body>
    </html>
    """

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            cur.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
            conn.commit()
        return redirect(url_for('guestbook'))

    cur.execute("SELECT content, created_at FROM messages ORDER BY created_at DESC")
    messages = cur.fetchall()
    cur.close()
    conn.close()

    html_list = "".join([f"<li style='margin-bottom:10px;'><b>{m[0]}</b> <br><small style='color:gray;'>{m[1]}</small></li>" for m in messages])
    
    return f"""
    <html>
        <body style="font-family: Arial; padding: 40px; line-height: 1.6;">
            <h1>Livre d'or 📖</h1>
            <form method="POST" style="margin-bottom: 30px;">
                <textarea name="content" placeholder="Laisse un message..." required style="width: 300px; height: 80px;"></textarea><br>
                <button type="submit" style="padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer;">Envoyer</button>
            </form>
            <hr>
            <h3>Messages récents :</h3>
            <ul>{html_list}</ul>
            <br><a href="/">⬅ Retour à l'accueil</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)