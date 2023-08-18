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

            output_filename = f'converted_image.{output_format.lower()}'
            output_image = input_image.copy()  # Make a copy before saving with the new format
            output_image.save(output_filename, format=output_format)

            return send_file(output_filename, as_attachment=True)

        return jsonify({'error': 'No file uploaded'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
