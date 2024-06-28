import json
import logging

from flask import Flask, request, jsonify
import os
import uuid
import datetime
import sys
from logging.handlers import TimedRotatingFileHandler

# Create log directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs', 'flask')
os.makedirs(log_dir, exist_ok=True)

handler = TimedRotatingFileHandler(
    os.path.join(log_dir, 'flask.log'),
    when='midnight',
    interval=1,
    backupCount=5
)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

app = Flask(__name__)
# UPLOAD_FOLDER = UPLOAD_FOLDER
# OUTPUT_FOLDER = OUTPUT_FOLDER
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(BASE_DIR, 'outputs'))
PORT = os.getenv('PORT', '5000')

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if send a file
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400

    # Check if the file has name
    file = request.files['file']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    #send to upload folder with requirement name
    if file:
        uid = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{file.filename}_{timestamp}_{uid}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        app.logger.info(f"File uploaded: {filename} with UID: {uid}")
        return jsonify({"uid": uid}), 200


@app.route('/status', methods=['GET'])
def check_status():
    uid = request.args.get('uid')
    if not uid:
        app.logger.error("UID is required")
        return jsonify({"error": "UID is required"}), 400

    upload_files = [f for f in os.listdir(UPLOAD_FOLDER) if uid in f]
    if upload_files:
        upload_file = upload_files[0]
        original_filename = '_'.join(upload_file.split('_')[:-2])
        timestamp = upload_file.split('_')[-2]
        app.logger.info(f"Status check: {uid} is pending")
        return jsonify({
            "status": "pending",
            "filename": original_filename,
            "timestamp": timestamp,
            "explanation": None
        }), 200

    # Check if the output file with the UID exists
    output_files = [f for f in os.listdir(OUTPUT_FOLDER) if uid in f]
    if output_files:
        # Assuming there's only one output file for each UID
        output_file = output_files[0]
        original_filename = '_'.join(output_file.split('_')[:-2])
        original_base_filename = os.path.splitext(original_filename)[0]
        timestamp = output_file.split('_')[-2]

        # Check if the JSON file exists
        json_filename = f"{original_base_filename}_{uid}.json"
        json_file_path = os.path.join(OUTPUT_FOLDER, json_filename)
        if os.path.exists(json_file_path):
            # Try reading the file as JSON
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    explanation_data = json.load(f)
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"Decoding error or JSON decode error: {e}")
                return jsonify({
                    "status": "pending",
                    "filename": original_filename,
                    "timestamp": timestamp,
                    "explanation": None
                }), 200

            # Extract only the explanations if it is valid JSON
            explanations = list(explanation_data.values())
            app.logger.info(f"Status check: {uid} is done")
            return jsonify({
                "status": "done",
                "filename": original_filename,
                "timestamp": timestamp,
                "explanation": explanations
            }), 200
    app.logger.error(f"UID {uid} not found")
    return jsonify({"status": "not found"}), 404



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=int(PORT), debug=True)
    app.run(host='0.0.0.0', port=int(PORT), debug=True)