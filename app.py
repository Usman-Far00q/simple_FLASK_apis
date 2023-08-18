import os
from flask import Flask
import config
import logging

from apis.image_converter import views as image_conv_api_views
from apis.text_translator import views as text_trans_api_views
from apis.qr_code_generator import views as qr_code_generate_api_views


logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object(config.my_flask_config_obj)
    return app


app = create_app()


@app.route('/home')
@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to simple APIS'


@app.route('/api/img-conv/convert', methods=['POST'])
def post_convert_image():
    return image_conv_api_views.convert_image()


@app.route('/api/txt-trans/translate', methods=['POST'])
def post_translate_text():
    return text_trans_api_views.translate_paragraph()


@app.route('/api/qr-gen/generate', methods=['POST'])
def post_generate_qr_code():
    return qr_code_generate_api_views.generate_qr_code()

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
