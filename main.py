from io import BytesIO
from flask import Flask, request, jsonify, send_file
from tempfile import NamedTemporaryFile
from rembg import remove
from PIL import Image

app = Flask(__name__)


@app.route('/removeBackground', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file uploaded'}), 400

        with NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
            image_file = request.files['image']
            image_file.save(temp_image)

        input = Image.open(temp_image.name)
        output_image = remove(input)

        output_image_bytes = BytesIO()
        output_image.save(output_image_bytes, format="PNG")
        output_image_bytes.seek(0)

        return send_file(output_image_bytes, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
