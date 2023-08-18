from flask import request, jsonify
from translate import Translator
from langdetect import detect_langs, DetectorFactory
from googletrans import LANGUAGES


def translate_paragraph():
    try:
        source_text = request.json.get('source_text')
        target_language = request.json.get('target_language', 'en')  # Default to English

        if not source_text:
            return jsonify({'error': 'No source text provided'}), 400

        DetectorFactory.seed = 0
        detected_languages = detect_langs(source_text)
        detected_language = detected_languages[0].lang

        detected_language_name = LANGUAGES.get(detected_language, 'Unknown')
        target_language_name = LANGUAGES.get(target_language, 'Unknown')

        if detected_language_name == 'Unknown':
            translator = Translator(to_lang=target_language)
        else:
            translator = Translator(from_lang=detected_language, to_lang=target_language)
        translated_text = translator.translate(source_text)

        response = {
            'detected_language': detected_language,
            'detected_language_name': detected_language_name,
            'target_language': target_language,
            'target_language_name': target_language_name,
            'translated_text': translated_text
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
