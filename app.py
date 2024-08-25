from flask import Flask, render_template, request, send_file, jsonify
import os
import cv2
from werkzeug.utils import secure_filename
from face import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

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

        # Get cropping coordinates
        crop_x = int(request.form.get('cropX', 0))
        crop_y = int(request.form.get('cropY', 0))
        crop_width = int(request.form.get('cropWidth', 0))
        crop_height = int(request.form.get('cropHeight', 0))

        # Load and crop the image
        image = cv2.imread(input_image_path)
        cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
        cv2.imwrite(input_image_path, cropped_image)

        # Process the cropped image
        face_detected, message = process_image(input_image_path, output_image_path)

        if face_detected:
            return jsonify({'status': 'success', 'output_image': output_image_path})
        else:
            return jsonify({'status': 'fail', 'message': message})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
