# oufrom flask import Flask, jsonify
vim app.py app = Flask(__name__)
# ou
code app.py  # si VS Code est installé@app.route('/')
def home():
    return jsonify({
        "message": "Hello from my DevOps App! 🚀",
        "status": "ok",
        "version": "1.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "running",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "pod": socket.gethostname()
    })
