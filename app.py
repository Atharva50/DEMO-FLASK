from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('API_KEY', 'demo-key-12345')

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Flask API for Oracle APEX Integration",
        "endpoints": ["/predict", "/health"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401
    
    try:
        data = request.get_json()
        
        if not data or 'amount' not in data:
            return jsonify({"error": "Missing 'amount' field"}), 400
        
        amount = float(data['amount'])
        tax = round(amount * 0.18, 2)
        total = round(amount + tax, 2)
        
        response = {
            "amount": amount,
            "tax": tax,
            "total": total,
            "message": "Success",
            "timestamp": "2025-11-11"
        }
        
        return jsonify(response), 200
        
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)