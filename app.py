from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SECRET_KEY'] = 'hackathon_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100))
    date = db.Column(db.String(50))
    purpose = db.Column(db.String(200))

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    time = db.Column(db.String(50))

# --- ROUTES ---

# 1. Landing / Login Page
@app.route('/')
def index():
    return render_template('index.html')

# 2. The Main Dashboard
@app.route('/dashboard')
def dashboard():
    appointments = Appointment.query.all()
    meds = Medication.query.all()
    return render_template('dashboard.html', appointments=appointments, meds=meds)

# 3. The "Innovation" Feature (Smart Scan)
# HACK: For the demo, we simulate OCR based on filenames.
@app.route('/upload_scan', methods=['POST'])
def upload_scan():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    filename = file.filename.lower()

    if filename == '':
        return redirect(request.url)

    # SIMULATION LOGIC FOR DEMO VIDEO
    if "prescription" in filename:
        # If they upload a file named "prescription.jpg", auto-add a medicine
        new_med = Medication(name="Amoxicillin (Auto-Detected)", dosage="500mg", time="After Dinner")
        db.session.add(new_med)
        db.session.commit()
        flash("Scan Successful! Medication extracted from image.")
    
    elif "summary" in filename:
        # If they upload "discharge_summary.jpg", auto-add an appointment
        new_appt = Appointment(doctor="Dr. Sharma (Cardio)", date="2026-01-10", purpose="Post-Op Checkup")
        db.session.add(new_appt)
        db.session.commit()
        flash("Scan Successful! Follow-up appointment detected.")
    
    else:
        flash("File uploaded to records vault.")

    return redirect(url_for('dashboard'))

# 4. Helper to reset DB (Run this once)
@app.route('/init_db')
def init_db():
    with app.app_context():
        db.create_all()
        # Add dummy data
        if not Appointment.query.first():
            db.session.add(Appointment(doctor="Dr. A. Patil", date="2026-01-05", purpose="Stitch Removal"))
            db.session.add(Medication(name="Paracetamol", dosage="650mg", time="Morning/Night"))
            db.session.commit()
    return "Database Initialized! Go to /dashboard"

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True,port =9999)