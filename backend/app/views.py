"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site 

from app import app, Config,  mongo, Mqtt
from flask import render_template, request, jsonify, send_file, redirect, make_response, send_from_directory 
from json import dumps, loads 
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta, timezone
from os import getcwd
from os.path import join, exists
from time import time, ctime
from math import floor

from markupsafe import escape



#####################################
#   Routing for your application    #
#####################################


# 1. CREATE ROUTE FOR '/api/set/combination'
@app.route('/api/set/combination', methods=['POST'])
def update_passcode():
    passcode = request.json.get('code')
    print(f"Passcode received: {passcode}")
    
    try:
        if mongo.setPass(passcode):  
            return jsonify({"status": "complete", "data": "Passcode updated"})
    except Exception as e:
        print(f"update_passcode error: {e}")
    
    return jsonify({"status": "failed", "data": "Database update failed"})

# 2. CREATE ROUTE FOR '/api/check/combination'
@app.route('/api/check/combination', methods=['POST'])
def check_passcode():
    """Checks if the passcode is correct"""
    try:
        passcode = request.form.get('passcode')
        if passcode and mongo.count_passcodes(passcode) != 0:
            return jsonify({"status": "success", "data": "complete"})
    except Exception as e:
        print(f"check_passcode error: {e}")
    
    return jsonify({"status": "failed", "data": "failed"})

# 3. CREATE ROUTE FOR '/api/update'
@app.route('/api/update', methods=['POST'])
def update_radar():
    """Updates the 'radar' collection"""
    try:
        jsonDoc = request.get_json()
        jsonDoc['timestamp'] = floor(datetime.now().timestamp())
        
        mqtt_payload = mongo.dumps(jsonDoc)
        Mqtt.publish("620160532", mqtt_payload)
        Mqtt.publish("620160532_sub", mqtt_payload)
        
        print(f"MQTT: {jsonDoc}")
        
        if mongo.insertData(jsonDoc):
            return jsonify({"status": "complete", "data": "complete"})
    except Exception as e:
        print(f"update_radar error: {e}")
    
    return jsonify({"status": "failed", "data": "failed"})

# 4. CREATE ROUTE FOR '/api/reserve/<start>/<end>'
@app.route('/api/reserve/<int:start>/<int:end>', methods=['GET'])
def get_reserve_radar(start, end):
    """Returns the 'reserve' field using all documents found between start and end timestamps"""
    try:
        result = list(mongo.retrieve_radar(start, end))
        if result:
            return jsonify({"status": "success", "data": result})
    except Exception as e:
        print(f"get_reserve_radar error: {e}")
    
    return jsonify({"status": "failed", "data": "failed"})

# 5. CREATE ROUTE FOR '/api/avg/<start>/<end>'
@app.route('/api/avg/<int:start>/<int:end>', methods=['GET'])
def get_average_radar(start, end):
    """Returns the average of the 'reserve' field using documents found between start and end timestamps"""
    try:
        result = list(mongo.average_radar(start, end))
        if result:
            return jsonify({"status": "success", "data": result})
    except Exception as e:
        print(f"get_average_radar error: {e}")
    
    return jsonify({"status": "failed", "data": "failed"})

# 6. SERVE FILE FROM UPLOADS DIRECTORY
@app.route('/api/file/get/<filename>', methods=['GET']) 
def get_images(filename):
    """Returns requested file from uploads folder"""
    directory = join(getcwd(), Config.UPLOADS_FOLDER)
    file_path = join(directory, filename)
    
    if exists(file_path):
        return send_from_directory(directory, filename)
    
    return jsonify({"status": "file not found"}), 404

# 7. UPLOAD FILE TO UPLOADS DIRECTORY
@app.route('/api/file/upload', methods=['POST'])  
def upload():
    """Saves a file to the uploads folder"""
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "failed", "data": "No file provided"})
    
    filename = secure_filename(file.filename)
    file.save(join(getcwd(), Config.UPLOADS_FOLDER, filename))
    return jsonify({"status": "File upload successful", "filename": filename})

# GLOBAL FLASK SETTINGS
@app.after_request
def add_header(response):
    """Forces latest rendering engine and prevents caching"""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 response"""
    return jsonify({"status": 404}), 404
