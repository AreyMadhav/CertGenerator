from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import os

UPLOAD_FOLDER = 'C:/Users/minec/Downloads/CertGen/uploads'

app = Flask(__name__)
app.secret_key = 'SecretKeyLOL'

# Configuration
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'  # New variable for templates folder
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['TEMPLATE_FOLDER'] = TEMPLATE_FOLDER  # New configuration for templates folder


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_text_to_image(image_path, name, output_path, font_path=None, font_size=30, text_color=(255, 255, 255),
                      position=(10, 10)):
    try:
        # Open the image
        image = Image.open(image_path)

        # Load a font
        if font_path is None:
            font = ImageFont.load_default()
        else:
            font = ImageFont.truetype(font_path, font_size)

        # Initialize drawing context
        draw = ImageDraw.Draw(image)

        # Add text to image
        draw.text(position, name, fill=text_color, font=font)

        # Save the modified image
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded username and password
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'

    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form data and generate certificates
        # Redirect to the app route after processing
        return redirect(url_for('app_page'))
    return render_template('index.html')


@app.route('/app')
def app_page():
    # Your app logic here
    return 'This is the app page'


@app.route('/logout')
def logout():
    # Handle logout logic here
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
