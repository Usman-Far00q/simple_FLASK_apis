from flask import request, jsonify, send_file
from qrcode.constants import ERROR_CORRECT_L
from qrcode.main import QRCode
from PIL import Image, ImageFilter, ImageChops
from io import BytesIO
import random


def generate_abstract_art(size):
    # Create a random-colored background
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    background = Image.new("RGB", size, (r, g, b))

    # TODO: the commented code below is responsible for that sudo Ai-ish effect on QR codes
    # background = make_abstract_art()

    abstract_art = background.filter(ImageFilter.GaussianBlur(radius=10))
    abstract_art = ImageChops.multiply(abstract_art, background)

    return abstract_art


def generate_qr_code():
    try:
        raw_url = request.json.get('raw_url')

        if not raw_url:
            return jsonify({'error': 'No raw URL provided'}), 400

        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(raw_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Generate abstract art image
        abstract_art = generate_abstract_art(img.size)

        # Resize the abstract art image to match the QR code size
        abstract_art = abstract_art.resize(img.size)

        # Create a new image by overlaying the QR code on the abstract art
        new_img = Image.blend(img, abstract_art, alpha=0.5)

        # TODO: Usman-you can use this code incase user ants to just make a simple black and white QR code
        # new_img = Image.blend(img, img, alpha=0.5)

        output_buffer = BytesIO()
        new_img.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return send_file(output_buffer, mimetype="image/png")

    except Exception as e:
        return jsonify({'error': str(e)}), 500
