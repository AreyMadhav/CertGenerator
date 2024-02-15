from flask import Flask, render_template, request, send_from_directory, flash, redirect
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.secret_key = 'SecretKeyLOL'

# Configuration
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


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
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        names = request.form.get('names').split(',')

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            for name in names:
                name = name.strip()
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                output_path = os.path.join(app.config['STATIC_FOLDER'], f'{name.replace(" ", "_")}_certificate.jpg')
                file.save(image_path)
                if add_text_to_image(image_path, name, output_path, font_path='arial.ttf'):
                    os.remove(image_path)
            return render_template('index.html', certificates=names)
        else:
            flash('Invalid file format. Allowed formats are jpg, jpeg, png')
            return redirect(request.url)

    return render_template('index.html', certificates=[])


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)
