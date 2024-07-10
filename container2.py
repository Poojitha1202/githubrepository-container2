from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

FILE_DIRECTORY = "/path_to_your_persistent_volume"

@app.route('/validate-csv', methods=['POST'])
def validate_csv():
    """API endpoint to validate if the file is a proper CSV."""
    data = request.get_json()
    filepath = f'/data/{data["file"]}'

    try:
        # Attempt to read the file as a CSV
        df = pd.read_csv(filepath)
        # Check for the necessary columns
        if 'product' in df.columns and 'amount' in df.columns:
            return jsonify({"file": data["file"], "message": "File is a valid CSV."}), 200
        else:
            return jsonify({"file": data["file"], "error": "CSV does not contain the required columns."}), 400
    except pd.errors.ParserError:
        return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400
    except FileNotFoundError:
        return jsonify({"file": data["file"], "error": "File not found."}), 404


@app.route('/processSum', methods=['POST'])
def computeSum():
    data = request.get_json()
    
    filepath = f'/data/{data["file"]}'

    product = data['product']
    
    try:
        df = pd.read_csv(filepath, delimiter=',')

        required_columns = ['product', 'amount']
        if not all(column in df.columns for column in ['product', 'amount']):
            return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400
        
        total_sum = df[df['product'] == product]['amount'].sum()
        
        return jsonify({"file": data["file"], "sum": int(total_sum)})
    except pd.errors.ParserError:
        return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400
    except pd.errors.EmptyDataError:
        return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)  # Use an internal port different from the orchestrator