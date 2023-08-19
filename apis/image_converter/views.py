from io import BytesIO

from flask import request, jsonify, send_file
from PIL import Image


ALLOWED_FORMATS = ['JPEG', 'PNG', 'GIF']  # Allowed output formats


def convert_image():
    try:
        file = request.files['file']
        output_format = request.form.get('format', 'JPEG').upper()

        if file and file.filename != '':
            if output_format not in ALLOWED_FORMATS:
                return jsonify({'error': 'Invalid output format'}), 400

            input_image = Image.open(file)

            if input_image.mode != 'RGB':
                input_image = input_image.convert('RGB')

            output_buffer = BytesIO()
            # convert and save image inside python-memory (Byte-stream) instead of on DISK
            input_image.save(output_buffer, format=output_format.lower())
            output_buffer.seek(0)
            return send_file(output_buffer, mimetype=f"image/{output_format.lower()}")

        return jsonify({'error': 'No file uploaded'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
