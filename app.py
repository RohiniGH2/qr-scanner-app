from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import qrcode
import json
import os
import socket
from datetime import datetime
import base64
from io import BytesIO
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/photos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'qr_scanner_secret_key_2025'  # Change this in production

# Create necessary directories
try:
    os.makedirs('static/photos', exist_ok=True)
    os.makedirs('static/qrcodes', exist_ok=True)
    print("✅ Directories created successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not create directories: {e}")

# Data file paths
DATA_FILE = 'students.json'
ADMIN_FILE = 'admins.json'

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_admins():
    """Load admins from JSON file"""
    try:
        if os.path.exists(ADMIN_FILE):
            with open(ADMIN_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading admins: {e}")
    return {}

def save_admins(admins):
    """Save admins to JSON file"""
    with open(ADMIN_FILE, 'w') as f:
        json.dump(admins, f, indent=2)

def check_admin_exists():
    """Check if any admin exists"""
    try:
        admins = load_admins()
        return len(admins) > 0
    except Exception as e:
        print(f"Error checking admin exists: {e}")
        return False

def login_required(f):
    """Decorator to require login for admin routes"""
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def load_students():
    """Load students from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_students(students):
    """Save students to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

def generate_unique_roll():
    """Generate unique roll number"""
    students = load_students()
    if not students:
        return "ROLL001"
    
    # Find highest existing roll number
    existing_rolls = [int(student['roll_number'][4:]) for student in students.values() 
                     if student['roll_number'].startswith('ROLL')]
    if existing_rolls:
        next_num = max(existing_rolls) + 1
    else:
        next_num = 1
    
    return f"ROLL{next_num:03d}"

def generate_qr_code(roll_number):
    """Generate QR code for student with appropriate URL"""
    # Check if we're in production (Render) or local development
    if 'PORT' in os.environ:
        # Production: Uses Render URL
        base_url = request.url_root.rstrip('/')
        qr_data = f"{base_url}/student/{roll_number}"
    else:
        # Local: Uses local IP
        qr_data = f"http://{local_ip}:{port}/student/{roll_number}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code image
    qr_filename = f"static/qrcodes/{roll_number}.png"
    img.save(qr_filename)
    
    # Also convert to base64 for immediate display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}", qr_filename

@app.route('/')
def index():
    """Redirect to login or dashboard based on authentication"""
    try:
        if not check_admin_exists():
            return redirect(url_for('register_form'))
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"<h1>QR Scanner App</h1><p>Setting up... <a href='/register'>Create Admin Account</a></p>"

@app.route('/register')
def register_form():
    """Show admin registration form"""
    try:
        # If admin already exists, redirect to login
        if check_admin_exists():
            return redirect(url_for('login'))
        return render_template('register.html')
    except Exception as e:
        print(f"Error in register_form: {e}")
        # Fallback: create a simple registration form
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Admin Registration</title></head>
        <body>
        <h2>Create Admin Account</h2>
        <form method="POST" action="/register">
            <p>Username: <input type="text" name="username" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <p>Confirm Password: <input type="password" name="confirm_password" required></p>
            <p>Full Name: <input type="text" name="full_name" required></p>
            <p>Email: <input type="email" name="email" required></p>
            <p><button type="submit">Register</button></p>
        </form>
        </body>
        </html>
        '''

@app.route('/register', methods=['POST'])
def register():
    """Process admin registration"""
    # If admin already exists, redirect to login
    if check_admin_exists():
        flash('Admin already exists. Please login.', 'warning')
        return redirect(url_for('login'))
    
    username = request.form['username'].strip()
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    full_name = request.form['full_name'].strip()
    email = request.form['email'].strip()
    
    # Validation
    if len(username) < 3:
        flash('Username must be at least 3 characters long.', 'error')
        return render_template('register.html')
    
    if len(password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return render_template('register.html')
    
    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return render_template('register.html')
    
    # Create admin
    admins = load_admins()
    admin_data = {
        'username': username,
        'password': hash_password(password),
        'full_name': full_name,
        'email': email,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'last_login': None
    }
    
    admins[username] = admin_data
    save_admins(admins)
    
    flash('Admin account created successfully! Please login.', 'success')
    return redirect(url_for('login'))

@app.route('/login')
def login_form():
    """Show login form"""
    # If no admin exists, redirect to registration
    if not check_admin_exists():
        return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Process admin login"""
    username = request.form['username'].strip()
    password = request.form['password']
    
    admins = load_admins()
    
    if username in admins and admins[username]['password'] == hash_password(password):
        session['admin_logged_in'] = True
        session['admin_username'] = username
        session['admin_full_name'] = admins[username]['full_name']
        
        # Update last login
        admins[username]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_admins(admins)
        
        flash(f'Welcome back, {admins[username]["full_name"]}!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password.', 'error')
        return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout admin"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing all students"""
    students = load_students()
    local_ip = get_local_ip()
    return render_template('index.html', students=students, local_ip=local_ip)

@app.route('/student/<roll_number>')
def student_detail(roll_number):
    """Show detailed view of a specific student"""
    students = load_students()
    student = students.get(roll_number)
    
    if not student:
        return render_template('error.html', 
                             message="Student not found", 
                             details=f"No student found with roll number: {roll_number}")
    
    return render_template('student_detail.html', student=student)

@app.route('/add_student')
@login_required
def add_student_form():
    """Show form to add new student"""
    return render_template('add_student.html')

@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    """Process new student addition"""
    students = load_students()
    
    # Generate unique roll number
    roll_number = generate_unique_roll()
    
    # Handle photo upload
    photo_filename = "default.jpg"
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '':
            filename = secure_filename(f"{roll_number}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_filename = filename
    
    # Create student data
    student_data = {
        "roll_number": roll_number,
        "name": request.form['name'],
        "class_year": request.form['class_year'],
        "department": request.form['department'],
        "date_of_birth": request.form['date_of_birth'],
        "guardian_name": request.form['guardian_name'],
        "guardian_phone": request.form['guardian_phone'],
        "address": request.form['address'],
        "email": request.form['email'],
        "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Active",
        "photo": photo_filename,
        "emergency_contact": request.form.get('emergency_contact', ''),
        "blood_group": request.form.get('blood_group', ''),
        "notes": request.form.get('notes', '')
    }
    
    # Generate QR code
    qr_base64, qr_filename = generate_qr_code(roll_number)
    student_data['qr_code'] = qr_filename
    
    # Save student
    students[roll_number] = student_data
    save_students(students)
    
    return redirect(url_for('dashboard'))

@app.route('/api/student/<roll_number>')
def api_student_detail(roll_number):
    """API endpoint to get student details"""
    students = load_students()
    student = students.get(roll_number)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)

@app.route('/edit_student/<roll_number>')
@login_required
def edit_student_form(roll_number):
    """Show form to edit existing student"""
    students = load_students()
    student = students.get(roll_number)
    
    if not student:
        return render_template('error.html', 
                             message="Student not found", 
                             details=f"No student found with roll number: {roll_number}")
    
    return render_template('edit_student.html', student=student)

@app.route('/edit_student/<roll_number>', methods=['POST'])
@login_required
def edit_student(roll_number):
    """Process student edit"""
    students = load_students()
    
    if roll_number not in students:
        return render_template('error.html', 
                             message="Student not found", 
                             details=f"No student found with roll number: {roll_number}")
    
    student = students[roll_number]
    
    # Handle photo upload (if new photo is provided)
    photo_filename = student['photo']  # Keep existing photo by default
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '':
            # Remove old photo if it's not default
            if student['photo'] != 'default.jpg':
                old_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], student['photo'])
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            
            # Save new photo
            filename = secure_filename(f"{roll_number}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_filename = filename
    
    # Update student data
    student.update({
        "name": request.form['name'],
        "class_year": request.form['class_year'],
        "department": request.form['department'],
        "date_of_birth": request.form['date_of_birth'],
        "guardian_name": request.form['guardian_name'],
        "guardian_phone": request.form['guardian_phone'],
        "address": request.form['address'],
        "email": request.form['email'],
        "photo": photo_filename,
        "emergency_contact": request.form.get('emergency_contact', ''),
        "blood_group": request.form.get('blood_group', ''),
        "notes": request.form.get('notes', ''),
        "status": request.form.get('status', 'Active')
    })
    
    # Save updated student data
    students[roll_number] = student
    save_students(students)
    
    return redirect(url_for('student_detail', roll_number=roll_number))

@app.route('/delete_student/<roll_number>')
@login_required
def delete_student(roll_number):
    """Delete a student"""
    students = load_students()
    if roll_number in students:
        # Remove photo and QR code files
        student = students[roll_number]
        if student['photo'] != 'default.jpg':
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], student['photo'])
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        qr_path = student.get('qr_code', '')
        if os.path.exists(qr_path):
            os.remove(qr_path)
        
        del students[roll_number]
        save_students(students)
    
    return redirect(url_for('dashboard'))

@app.route('/test')
def test_connection():
    """Simple test endpoint for mobile connectivity"""
    return jsonify({
        "status": "success",
        "message": "Mobile connection working!",
        "server_ip": get_local_ip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/network-info')
def network_info():
    """Provide network diagnostic information"""
    local_ip = get_local_ip()
    return f"""
    <html>
    <head>
        <title>Network Diagnostic</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
            .success {{ color: #28a745; font-weight: bold; }}
            .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            .url {{ background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🎉 Mobile Connection Successful!</h2>
            <p class="success">✅ Your phone can reach the Flask server!</p>
            
            <div class="info">
                <h3>📊 Network Information:</h3>
                <p><strong>Server IP:</strong> {local_ip}</p>
                <p><strong>Server Port:</strong> 8080</p>
                <p><strong>Timestamp:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="info">
                <h3>🔗 Available URLs:</h3>
                <p><strong>Main Application:</strong></p>
                <div class="url">http://{local_ip}:8080/</div>
                
                <p><strong>Test Connection:</strong></p>
                <div class="url">http://{local_ip}:8080/test</div>
                
                <p><strong>Student Example:</strong></p>
                <div class="url">http://{local_ip}:8080/student/ROLL001</div>
            </div>
            
            <div class="info">
                <h3>📱 QR Code Access:</h3>
                <p>Your QR codes should now work! Try scanning them with your phone's camera.</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Use environment port for production (Render) or default for local
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'
    
    # Get local IP for local development info
    local_ip = get_local_ip()
    
    if 'PORT' in os.environ:
        # Production mode (Render)
        print(f"🚀 Starting production server on port {port}")
        app.run(host=host, port=port, debug=False)
    else:
        # Local development mode
        print(f"🔧 Starting development server on {local_ip}:{port}")
        print(f"Access from any device on your LAN: http://{local_ip}:{port}")
        print(f"Test connectivity: http://{local_ip}:{port}/test")
        app.run(host=host, port=port, debug=True)
