from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "project": "AutoDeploy360",
        "author": "Moin Pasha",
        "version": "2.0"
    })

@app.route('/health')
def health():
    return jsonify({"health": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)