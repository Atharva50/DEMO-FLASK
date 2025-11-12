from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # ✅ Enables CORS globally so Oracle APEX can call this API

# ✅ Use environment variable or fallback default
API_KEY = os.getenv('API_KEY', 'demo-key-12345')

@app.route('/')
def home():
    """Health check route"""
    return jsonify({
        "status": "online",
        "message": "Flask API for Oracle APEX Integration",
        "endpoints": ["/predict"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Main API endpoint for tax + total calculation"""
    api_key = request.headers.get('X-API-KEY')

    # ✅ API Key check
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    try:
        # ✅ Parse JSON body safely
        data = request.get_json(force=True, silent=True)
        if not data or 'amount' not in data or 'tax' not in data:
            return jsonify({"error": "Missing 'amount' or 'tax' field"}), 400

        # ✅ Business logic
        amount = float(data['amount'])
        tax = float(data['tax'])
        total = round(amount + tax, 2)

        # ✅ Response
        return jsonify({
            "amount": amount,
            "tax": tax,
            "total": total,
            "message": "Success",
            "timestamp": "2025-11-12"
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ For Render or local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
