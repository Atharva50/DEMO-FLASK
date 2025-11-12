@app.route('/predict', methods=['POST'])
def predict():
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    try:
        # ✅ Force JSON parse to avoid NoneType issues
        data = request.get_json(force=True, silent=True)

        # ✅ Validation
        if not data or 'amount' not in data or 'tax' not in data:
            return jsonify({"error": "Missing 'amount' or 'tax' field"}), 400

        amount = float(data['amount'])
        tax = float(data['tax'])
        total = round(amount + tax, 2)

        response = {
            "amount": amount,
            "tax": tax,
            "total": total,
            "message": "Success",
            "timestamp": "2025-11-12"
        }

        return jsonify(response), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
