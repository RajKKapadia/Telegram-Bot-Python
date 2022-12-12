from outside_apis.openai_api import text_complition
from outside_apis.telegram_api import send_message, set_webhook, set_menu_commands
from helper.utils import process_request
import os

from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


HEADER_TOKEN = os.getenv('HEADER_TOKEN')


@app.route('/telegram', methods=['POST'])
def telegram_api():

    if request.is_json:

        data = process_request(request=request)

        if data['secret_token'] == HEADER_TOKEN:

            if data['is_text']:
                result = text_complition(data['message'])
                if result['status'] == 1:
                    _ = send_message(data['sender_id'], result['response'])
                    return 'OK', 200
                else:
                    return 'SERVER ERROR', 200
            else:
                _ = send_message(data['sender_id'], 'Hey, that is great, but I only understand text and commands at this time.')

        return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400


@app.route('/set-telegram-webhook', methods=['POST'])
def set_telegram_webhook():

    if request.is_json:

        body = request.get_json()

        flag = set_webhook(body['url'], body['secret_token'])

        if flag:
            return 'OK', 200
        else:
            'BAD REQUEST', 400
    else:
        'BAD REQUEST', 400


@app.route('/set-telegram-menu-commands', methods=['POST'])
def set_telegram_menu_commands():

    if request.is_json:

        body = request.get_json()

        flag = set_menu_commands(body['commands'])

        if flag:
            return 'OK', 200
        else:
            'BAD REQUEST', 400
    else:
        'BAD REQUEST', 400
