# Import modules
from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from main import app
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import secrets
import string

# Load environment variables into module
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PREDICTION_THRESHOLD'] = os.getenv('PREDICTION_THRESHOLD', 80)
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/uploads')
app.config['RESULT_FOLDER'] = os.path.join(basedir, 'static/results')
app.config['MODEL'] = os.path.join(basedir, 'static/models/yolov8n_modified.pt')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_random_filename(extension="", length=16):
    characters = string.ascii_letters + string.digits
    random_filename = ''.join(secrets.choice(characters) for i in range(length))
    
    if extension:
        random_filename += f".{extension}"
    
    return random_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            img = cv2.imread(file_path)
            
            model = YOLO(app.config['MODEL'])
            detections = model(img)
            
            if len(detections) > 0:
                result = detections[0]
                boxes = result.boxes
                detected_objects = []

                for box in boxes:
                    class_id = int(box.data[0][-1])
                    class_name = model.names[class_id]
                    confidence = float(box.conf.cpu().numpy()) 

                    if confidence > (int(app.config['PREDICTION_THRESHOLD']) / 100):
                        detected_objects.append({
                            "class": class_name,
                            "confidence": confidence
                        })

                img_annot = result.plot()
                img_name = generate_random_filename(extension='jpg', length=32)

                dest_directory = app.config['RESULT_FOLDER']
                cv2.imwrite(f'{dest_directory}/{img_name}', img_annot)
                print(detected_objects)

            return render_template('index.html')
        
    return render_template('index.html')