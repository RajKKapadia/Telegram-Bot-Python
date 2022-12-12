from flask import request

def processRequest(request: request) -> dict:
    body = request.get_json()
    sender_id = body['message']['from']['id']
    user_name = body['message']['from']['username']
    message = body['message']['text']
    headers = request.headers
    secret_token = headers['X-Telegram-Bot-Api-Secret-Token']

    return {
        'sender_id': sender_id,
        'user_name': user_name,
        'message': message,
        'secret_token': secret_token
    }