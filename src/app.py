import os

from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

from helper.utils import processRequest
from outside_apis.telegram_api import sendMessage
from outside_apis.openai_api import textComplition


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


HEADER_TOKEN = os.getenv('HEADER_TOKEN')


@app.route('/telegram', methods=['POST'])
def telegram_api():
    if request.is_json:

        data = processRequest(request=request)

        if data['secret_token'] == HEADER_TOKEN:

            result = textComplition(data['message'])

            if result['status'] == 1:
                _ = sendMessage(data['sender_id'], result['response'])
                return 'OK', 200
            else:
                return 'SERVER ERROR', 200

        return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400


@app.route('/set-webhook', methods=['POST'])
def set_webhook():
    url_root = request.url_root
    webhook_url = f'{url_root}telegram'
    print(webhook_url)
    return 'OK', 200
