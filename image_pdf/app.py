from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import zipfile

app = Flask(__name__)

# Create directories for uploads and converted files if they don't exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('converted', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'images' not in request.files:
        return "No file part"
    files = request.files.getlist('images')
    if not files or files[0].filename == '':
        return "No selected files"

    conversion_type = request.form.get('conversion-type')

    # PDF Settings
    paper_size = request.form.get('paper-size')
    orientation = request.form.get('orientation')
    margin = float(request.form.get('margin', 1.0))
    quality = request.form.get('quality')

    pdf_paths = []

    if conversion_type == 'single':
        pdf_path = os.path.join('converted', 'merged.pdf')
        images = []
        for file in files:
            image_path = os.path.join('uploads', file.filename)
            file.save(image_path)
            image = Image.open(image_path)
            images.append(image.convert('RGB'))
        images[0].save(pdf_path, save_all=True, append_images=images[1:], quality=quality, resolution=100.0, optimize=True, dpi=(300, 300))
        return send_file(pdf_path, as_attachment=True)

    elif conversion_type == 'multiple':
        for file in files:
            image_path = os.path.join('uploads', file.filename)
            file.save(image_path)
            pdf_path = os.path.join('converted', os.path.splitext(file.filename)[0] + '.pdf')
            image = Image.open(image_path)
            image.convert('RGB').save(pdf_path, quality=quality, resolution=100.0, optimize=True, dpi=(300, 300))
            pdf_paths.append(pdf_path)

        zip_path = os.path.join('converted', 'images_to_pdfs.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for pdf_path in pdf_paths:
                zipf.write(pdf_path, os.path.basename(pdf_path))
        return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
