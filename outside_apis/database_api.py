import os
from datetime import datetime


from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


client = MongoClient(os.getenv('CONNECTION_STRING'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]


def create_user(user: dict) -> bool:
    '''
    Create a new user

    Parameters:
        - user(dict)

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection.find_one(
        {
            'telegram_id': user['telegram_id']
        }
    )

    if not result:
        result = collection.insert_one(user)
        return result.acknowledged
    return False


def insert_message(telegram_id: int, message: dict) -> bool:
    '''
    Update messages for the user

    Parameters:
        - telegram_id(int): user telegram id
        - message(dict): mesage document to insert

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection.find_one_and_update(
        {
            'telegram_id': telegram_id
        },
        {
            '$push': {
                'messages': message
            }
        }
    )

    if not result:
        return False
    else:
        return True


def save_message_to_db(data: dict, response: str) -> bool:
    '''
    Process thewhole body and update the db

    Parameters:
        - data(dict): the incoming request from Telegram

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    message = {
        'query': data['message'],
        'response': response,
        'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }

    user = {
        'first_name': data['first_name'],
        'telegram_id': data['sender_id'],
        'messages': [message]
    }

    result = create_user(user)

    if result:
        return True
    else:
        result = insert_message(data['sender_id'], message)
        return result
