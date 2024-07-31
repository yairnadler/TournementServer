import json
from flask import Flask, request, jsonify
import logging
from utils import *
from bson import json_util

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/tournement', methods=['POST'])
def create_tournement():
    if request.content_type != 'application/json':
        return jsonify('error: Content-Type should be application/json'), 415
    
    data = request.get_json()
    valid, error = validate_tournement_data(data)

    if not valid:
        return jsonify({'error': error}), 422
    try:
        tournement_data = build_tournement(data)

        return jsonify(tournement_data), 201
    
    except Exception as e:
        # logging.error(f"Error building tournement: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/tournement/<tournement_id>', methods=['GET'])
def get_tournement(tournement_id):
    try:
        tournement = get_tournement_by_id(tournement_id)
        
        if tournement:
            return jsonify(tournement), 200
        else:
            return jsonify({'error': 'Tournement not found'}), 404
    
    except Exception as e:
        # logging.error(f"Error getting tournement: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/tournement/<tournement_id>/matches', methods=['GET'])
def get_matches(tournement_id):
    try:
        matches = get_matches_by_id(tournement_id)
        
        if matches:
            return jsonify(matches), 200
        else:
            return jsonify({'error': 'Matches not found'}), 404
    
    except Exception as e:
        # logging.error(f"Error getting matches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

        
    
    

    