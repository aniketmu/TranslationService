from flask import Flask, request, render_template, jsonify
import json
import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.form['text']
        language = request.form['language']

        key = os.environ['KEY']
        location = os.environ['LOCATION']
        endpoint = os.environ['ENDPOINT']

        path = 'translate'
        url = endpoint + path

        params = {
            'api-version' : '3.0',
            'to': language
        }

        headers={
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-Type': "application/json",
            'X-ClientTraceId': str(uuid.uuid4())
        }


        body = [{'text': text}]

        response = requests.post(url, params=params, headers=headers, json=body)

        data = response.json()

        tranlated_text = data[0]['translations'][0]['text']

        return render_template('results.html', original_text = text, translated_text=tranlated_text, language=language)

    except request.exceptions.RequestException as e:
        return jsonify({"message": "Failed to communicate with the translation Service", "error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Soemthing unexpected happened", "error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


if __name__ == '__main__':
    app.run(debug=True)