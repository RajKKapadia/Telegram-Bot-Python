from flask import request


def process_request(request: request) -> dict:
    '''
    Process the incoming data of the Telegram request
    '''
    
    body = request.get_json()
    sender_id = body['message']['from']['id']
    user_name = body['message']['from']['username']
    headers = request.headers
    secret_token = headers['X-Telegram-Bot-Api-Secret-Token']

    is_text = False

    if 'text' in body['message'].keys():
        message = body['message']['text']
        is_text = True

    return {
        'is_text': is_text,
        'sender_id': sender_id,
        'user_name': user_name,
        'message': message,
        'secret_token': secret_token
    }
