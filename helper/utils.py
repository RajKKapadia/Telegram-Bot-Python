import json

from flask import request

from outside_apis.openai_api import chat_complition


def process_request(body: dict) -> dict:
    '''
    Process the incoming data of the Telegram request

    Parameters:
        - body(dict)

    Returns:
        - dict of these key and value 
        {
            'is_text': is_text,
            'is_chat_deleted': is_chat_deleted,
            'sender_id': sender_id,
            'message': message,
            'secret_token': secret_token,
            'first_name': first_name
        }
    '''

    body = request.get_json()
    headers = request.headers
    secret_token = headers['X-Telegram-Bot-Api-Secret-Token']

    message = ''
    is_bot = True
    is_text = False
    first_name = ''
    sender_id = None

    if 'message' in body.keys():
        sender_id = body['message']['from']['id']
        first_name = body['message']['from']['first_name']
        is_bot = body['message']['from']['is_bot']

        if 'text' in body['message'].keys():
            message += body['message']['text']
            is_text = True

    return {
        'is_text': is_text,
        'sender_id': sender_id,
        'message': message,
        'secret_token': secret_token,
        'first_name': first_name,
        'is_bot': is_bot
    }


def generate_response(message: str) -> str:
    '''
    Process the incoming message for different command and generate a response string

    Parameters:
        - message(str): incoming message from Telegram

    Returns:
        - str: formated response for the command
    '''
    with open('responses.json') as file:
        data = json.loads(file.read())
    if message in data.keys():
        return data[message]
    else:
        result = chat_complition(message)
        if result['status'] == 1:
            return result['response'].strip()
        else:
            return 'Sorry, I am out of service at this moment.'
