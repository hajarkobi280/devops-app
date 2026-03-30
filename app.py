from flask import Flask, request, redirect, url_for, render_template_string
import psycopg2
from psycopg2 import pool
import os
import logging

app = Flask(__name__)

# Config & Logging
logging.basicConfig(level=logging.INFO)
DB_HOST = os.environ.get('DB_HOST', 'postgres-service')
DB_NAME = os.environ.get('DB_NAME', 'devopsdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'mypassword')

# Connection Pool (Optimisation Master)
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
except Exception as e:
    logging.error(f"Erreur Pool: {e}")

# --- TEMPLATES CSS/HTML (Design Moderne) ---
BASE_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>DevOps Master Project</title>
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background-color: #2c3e50; shadow: 0 2px 4px rgba(0,0,0,.1); }
        .card { border: none; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .btn-primary { background-color: #3498db; border: none; }
        .hero-section { background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; padding: 60px 0; border-radius: 0 0 50px 50px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark mb-0">
        <div class="container">
            <span class="navbar-brand mb-0 h1">Cloud & Big Data Architecture</span>
        </div>
    </nav>
    {% block content %}{% endblock %}
    <footer class="text-center mt-5 pb-4 text-muted">
        <small>Projet Master DSBD - Faculté des Sciences Ben M'sik-kobi Hajar-Benmijou Maroua © 2026</small>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (ts) VALUES (now());")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]
    db_pool.putconn(conn)
    
    content = f"""
    <div class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 fw-bold">Système Distribué Kubernetes</h1>
            <p class="lead">Dashboard d'analyse en temps réel</p>
        </div>
    </div>
    <div class="container mt-n5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card p-5 text-center mt-4">
                    <h3 class="text-secondary">Statistiques de Trafic</h3>
                    <div class="display-1 fw-bold text-primary my-3">{count}</div>
                    <p class="text-muted">Visites persistantes dans PostgreSQL</p>
                    <hr>
                    <div class="d-grid gap-2 d-md-flex justify-content-center mt-4">
                        <a href="/guestbook" class="btn btn-primary btn-lg px-4 me-md-2">Consulter le Livre d'Or</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_HTML.replace('{% block content %}{% endblock %}', content))

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    conn = db_pool.getconn()
    cur = conn.cursor()
    if request.method == 'POST':
        msg = request.form.get('content')
        if msg:
            cur.execute("INSERT INTO messages (content) VALUES (%s)", (msg,))
            conn.commit()
        return redirect(url_for('guestbook'))

    cur.execute("SELECT content, created_at FROM messages ORDER BY created_at DESC LIMIT 5")
    msgs = cur.fetchall()
    db_pool.putconn(conn)

    list_html = "".join([f'<div class="list-group-item"><strong>{m[0]}</strong><br><small class="text-muted">{m[1].strftime("%H:%M:%S")}</small></div>' for m in msgs])
    
    content = f"""
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card p-4">
                    <h2 class="mb-4">Livre d'Or 📖</h2>
                    <form method="POST" class="mb-4">
                        <div class="mb-3">
                            <textarea name="content" class="form-control" placeholder="Laissez un message technique ou un feedback..." rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Publier le message</button>
                    </form>
                    <div class="list-group">
                        {list_html}
                    </div>
                    <a href="/" class="btn btn-link mt-3 text-decoration-none">← Retour au Dashboard</a>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_HTML.replace('{% block content %}{% endblock %}', content))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)