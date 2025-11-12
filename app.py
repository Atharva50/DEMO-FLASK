from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Default API key (Render can override this via Environment variable)
API_KEY = os.environ.get('API_KEY', 'demo-key-12345')

@app.route('/')
def home():
    """Health info and available endpoints"""
    return jsonify({
        "status": "online",
        "message": "Flask API for Oracle APEX Integration",
        "endpoints": ["/predict", "/health"]
    }), 200


@app.route('/health')
def health():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Main API for tax + total calculation"""
    try:
        # ✅ 1. Validate API key
        api_key = request.headers.get('X-API-KEY')
        if api_key != API_KEY:
            return jsonify({"error": "Invalid API Key"}), 401

        # ✅ 2. Parse incoming JSON
        # Using force=True ensures data parses even if headers are missing
        data = request.get_json(force=True)

        if not data or 'amount' not in data:
            return jsonify({"error": "Missing 'amount' field"}), 400

        # ✅ 3. Business logic
        amount = float(data['amount'])
        tax = round(amount * 0.18, 2)
        total = round(amount + tax, 2)

        # ✅ 4. Response
        response = {
            "amount": amount,
            "tax": tax,
            "total": total,
            "message": "Success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(response), 200

    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
