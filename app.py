from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from face import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Route for serving the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for processing the image
@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No file part'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + filename)

        file.save(input_image_path)

        # Process the image
        success, message = process_image(input_image_path, output_image_path)

        if success:
            return jsonify({'status': 'success', 'output_image': output_image_path, 'message': message})
        else:
            return jsonify({'status': 'fail', 'message': message})

# Route to serve the processed image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
