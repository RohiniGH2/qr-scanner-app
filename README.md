# QR Scanner Flask App

A professional student management system with QR code generation and scanning capabilities.

## 🌟 Features

- 👥 Student Management (Add, Edit, Delete)
- 📱 QR Code Generation for each student
- 🔐 Admin Authentication
- 📊 Dashboard with Statistics
- 📱 Mobile-Responsive Design
- 🌐 Cross-device QR Code Scanning

## 🚀 Deploy to Render (Recommended)

### Quick Steps:

1. **Create GitHub Repository:**
   - Create a new repository on GitHub
   - Upload all your files to the repository

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** qr-scanner-app (or your choice)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
   - Click "Create Web Service"

3. **✅ Your app will be live at:** `https://your-app-name.onrender.com`

### Why Render?
- ✅ **No local network issues**
- ✅ **Works from anywhere**
- ✅ **Free tier available**
- ✅ **Automatic HTTPS**
- ✅ **No firewall configuration needed**

## 💻 Local Development (Alternative)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access at `http://localhost:8080`

## � Default Admin Account

- **Username:** admin
- **Password:** admin123

**⚠️ Change the default password immediately after first login!**

## 📁 File Structure

```
QR Scanner/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Render deployment config
├── templates/
│   └── index.html     # Main dashboard template
└── static/
    ├── photos/        # Student photos
    └── qrcodes/       # Generated QR codes
```

## 🆘 Troubleshooting

If you encounter issues:
1. Check the logs in Render dashboard
2. Ensure all files are properly uploaded
3. Verify the start command is `python app.py`
4. Make sure `requirements.txt` is in the root directory

## 🎯 Benefits of Cloud Deployment

- **Universal Access:** Works from any device with internet
- **No Network Configuration:** No need to mess with firewalls or local IP addresses
- **Professional URLs:** Clean, shareable links
- **Always Available:** 24/7 uptime
- **Mobile-Friendly:** Perfect QR code scanning from any phone
- **Auto Roll Numbers**: ROLL001, ROLL002, etc.
- **Photo Upload**: Student profile pictures
- **Detailed Information**: Guardian details, emergency contacts, medical info

### 📱 Mobile Optimized
- **Mobile-First Design**: Optimized for scanning devices (phones/tablets)
- **Touch-Friendly**: Large buttons, easy navigation
- **Quick Actions**: Call, email, share, print directly from mobile
- **Offline-Ready**: Works without internet once loaded

## 🏗️ Project Structure

```
QR Scanner/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── students.json             # Student data storage (auto-created)
├── templates/
│   ├── index.html            # Main dashboard (3-column layout)
│   ├── student_detail.html   # Detailed student profile (mobile-optimized)
│   ├── add_student.html      # Add new student form
│   └── error.html           # Error page
└── static/
    ├── photos/              # Student profile photos
    └── qrcodes/            # Generated QR code images
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access from Network Devices
The application will display your LAN IP address, for example:
```
Starting server on 192.168.1.100:5000
Access from any device on your LAN: http://192.168.1.100:5000
```

### 4. Add Students & Generate QR Codes
1. Open the dashboard on your computer
2. Click "Add Student" 
3. Fill in student details
4. QR code is automatically generated
5. Print or share QR codes as needed

### 5. Scan QR Codes
1. Use any mobile device on the same network
2. Scan the QR code with camera app or QR scanner
3. View detailed student information instantly

## 📋 Student Information Fields

### Basic Information
- **Name**: Full student name
- **Roll Number**: Auto-generated (ROLL001, ROLL002...)
- **Photo**: Profile picture upload
- **Class/Year**: Academic level
- **Department/Stream**: Subject specialization

### Personal Details
- **Date of Birth**: Student's DOB
- **Blood Group**: Medical information
- **Email**: Student email address
- **Address**: Residential address
- **Emergency Contact**: Additional contact number

### Guardian Information
- **Guardian Name**: Parent/guardian full name
- **Guardian Phone**: Primary contact number

### Additional
- **Enrollment Date**: Auto-recorded when added
- **Status**: Active/Inactive
- **Special Notes**: Medical conditions, allergies, etc.

## 🔧 Technical Details

### Backend
- **Framework**: Flask (Python)
- **Data Storage**: JSON file (easily upgradeable to database)
- **QR Generation**: `qrcode` library with PIL
- **File Uploads**: Werkzeug secure filename handling

### Frontend
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Responsive**: Mobile-first design
- **JavaScript**: Vanilla JS for interactions

### Network Architecture
- **Host**: `0.0.0.0` (all network interfaces)
- **Port**: `5000` (configurable)
- **LAN Only**: No external internet access required
- **Auto IP Detection**: Automatically detects local IP address

## 🎯 Use Cases

### 🏫 Educational Institutions
- **Attendance Tracking**: Quick student identification
- **Library Management**: Book checkout/return
- **Event Check-ins**: School events, exams, activities
- **Parent-Teacher Meetings**: Instant access to student info

### 🏢 Organizations
- **Employee ID System**: Staff identification
- **Training Programs**: Participant management
- **Visitor Management**: Guest registration and tracking

### 🏥 Healthcare/Emergency
- **Patient Identification**: Quick access to medical info
- **Emergency Contacts**: Instant guardian contact details
- **Medical History**: Blood group, allergies, conditions

## 📱 Mobile Experience

### Scanning Process
1. **Open QR Scanner**: Any camera app or QR scanner
2. **Point & Scan**: Aim at student's QR code
3. **Auto-Redirect**: Opens student profile in mobile browser
4. **Full Details**: View complete student information
5. **Quick Actions**: Call, email, share directly

### Mobile Features
- **Touch-Optimized**: Large buttons, easy scrolling
- **Offline Capable**: Works without internet after initial load
- **Share Integration**: Native mobile sharing
- **Print Support**: Mobile-friendly printing
- **Haptic Feedback**: Touch vibrations (if supported)

## 🔒 Security & Privacy

### LAN-Only Operation
- **Network Isolation**: Only works on local network
- **No Internet Dependency**: Completely offline system
- **Private Data**: Student information stays on local network
- **Controlled Access**: Only devices on same network can access

### Data Protection
- **Local Storage**: All data stored locally in JSON format
- **No Cloud**: No external data transmission
- **Secure Upload**: Filename sanitization for photo uploads
- **Session Control**: Flask session management

## 🛠️ Customization Options

### Adding New Fields
Edit `app.py` to add new student data fields:
```python
student_data = {
    "roll_number": roll_number,
    "name": request.form['name'],
    # Add your custom fields here
    "custom_field": request.form['custom_field'],
}
```

### Changing QR Code Design
Modify the `generate_qr_code()` function in `app.py`:
```python
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,  # Change error correction
    box_size=15,  # Change QR code size
    border=6,     # Change border size
)
```

### Database Upgrade
Replace JSON storage with SQLite/PostgreSQL:
1. Install database library (`sqlite3` or `psycopg2`)
2. Replace `load_students()` and `save_students()` functions
3. Add database initialization code

## 🔧 Troubleshooting

### Common Issues

**QR Codes Don't Work**
- Ensure both devices are on the same WiFi network
- Check if IP address has changed (restart app if needed)
- Verify firewall isn't blocking port 5000

**Photos Not Loading**
- Check `static/photos/` directory permissions
- Ensure uploaded images are valid formats (JPG, PNG)
- Verify file size is under 16MB limit

**Can't Access from Mobile**
- Double-check the IP address shown in terminal
- Try accessing `http://[IP]:5000` directly in mobile browser
- Ensure mobile device is on same WiFi network

### Network Configuration
```bash
# Check your IP address
ipconfig          # Windows
ifconfig          # Mac/Linux
ip addr show      # Linux

# Test connectivity
ping [IP_ADDRESS]  # From mobile device
```

## 🚀 Future Enhancements

### Database Integration
- SQLite for better data management
- PostgreSQL for larger institutions
- Data backup and restore features

### Advanced Features
- **Bulk Import**: CSV/Excel student data import
- **Attendance Logging**: Track scan times and locations
- **Reports**: Generate attendance and activity reports
- **Multi-User**: Admin accounts with different permissions
- **API Integration**: Connect with existing school management systems

### Mobile App
- Native Android/iOS app for better scanning
- Offline synchronization
- Push notifications
- Barcode scanning support

## 📞 Support

For technical support or feature requests:
1. Check the troubleshooting section above
2. Review the code comments in `app.py`
3. Test with sample data first
4. Ensure all dependencies are properly installed

## 📄 License

This project is designed for educational and institutional use. Feel free to modify and adapt according to your specific requirements.

---

**Ready to get started?** Run `python app.py` and begin adding your first students! 🎓
