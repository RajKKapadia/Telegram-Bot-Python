import os
import json


from outside_apis.telegram_api import send_message, set_webhook, set_menu_commands
from helper.utils import process_request, generate_response
from outside_apis.database_api import get_user, create_user, update_messages, create_payment, get_all_user


from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/telegram', methods=['POST'])
def telegram_api():
    # Make sure the request has json body
    with open('responses.json') as file:
        responses_data = json.loads(file.read())
    if request.is_json:
        body = request.get_json()
        data = process_request(body)
        # Make sure that the request is from Telegram
        if data['secret_token'] == os.getenv('HEADER_TOKEN'):
            # Make sure the request has text and is not from a Telegram bot
            if data['is_text'] and not data['is_bot']:
                # Check user exists
                user = get_user(data['sender_id'])
                if user:
                    # Check for the message count
                    if user['message_count'] > 0:
                        # Generate response
                        response = generate_response(data['message'])
                        # Update messages in MongoDB
                        message_count = user['message_count'] - 1
                        update_messages(data['sender_id'], data['message'], response, message_count)
                        # Send message through Telegram APIs
                        _ = send_message(data['sender_id'], response)
                        if message_count == 0:
                            _ = send_message(data['sender_id'], responses_data['subscribe'])
                        else:
                            _ = send_message(data['sender_id'], f'You have now {message_count} free messages.')
                    # Not enough messages, then send a message to subscribe
                    else:
                        if data['message'] in responses_data.keys():
                            response = generate_response(data['message'])
                            _ = send_message(data['sender_id'], response)
                        _ = send_message(data['sender_id'], responses_data['subscribe'])
                # IF user does not exists
                else:
                    response = generate_response(data['message'])
                    create_user(data, response)
                    _ = send_message(data['sender_id'], response)
            # Message is from bot, send myself an alert
            elif data['is_bot']:
                response = 'I know you are a bot.'
                _ = send_message(data['sender_id'], response)
            # For everything else coming to the bot, IGNORE
            else:
                pass
            return 'OK', 200
        # Request from unauthenticated source, send myself an alert
        _ = send_message(os.getenv('ME'), 'Unauthenticated request on the Webhook.')
        return 'OK', 200
    else:
        _ = send_message(os.getenv('ME'), 'Fire in the whole.')
        return 'OK', 200


@app.route('/set-telegram-webhook', methods=['POST'])
def set_telegram_webhook():
    if request.is_json:
        body = request.get_json()
        flag = set_webhook(body['url'], body['secret_token'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400


@app.route('/set-telegram-menu-commands', methods=['POST'])
def set_telegram_menu_commands():
    if request.is_json:
        body = request.get_json()
        flag = set_menu_commands(body['commands'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400
    
@app.route('/receive/payment', methods=['POST'])
def receive_payment():
    if request.is_json:
        body = request.get_json()
        create_payment(body)
        _ = send_message(os.getenv('ME'), 'New payment received.')
    else:
        pass
    return 'OK', 200

@app.route('/send/all', methods=['POST'])
def send_all():
    if request.is_json:
        body = request.get_json()
        sender_ids = get_all_user()
        if len(sender_ids) > 0:
            for id in sender_ids:
                _ = send_message(id, body['message'])
    else:
        pass
    return 'OK', 200

@app.route('/send/one', methods=['POST'])
def send_one():
    if request.is_json:
        body = request.get_json()
        _ = send_message(body['sender_id'], body['message'])
    else:
        pass
    return 'OK', 200
