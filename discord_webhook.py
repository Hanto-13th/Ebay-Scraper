import requests
import os
from dotenv import load_dotenv

#load the .env
load_dotenv()

def send_the_log(message_to_send):
    """This function send the complete analyzed from user requests into a user discord server using webhook.
    It takes in argument: the complete analyzed data to post"""
    #get the URL from the .env
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    #load the content of message and bot settings (Formated in JSON)
    data = {
    'content': f'{message_to_send}',
    'username': 'Log Scraper'
    }
    #post the request using URl and payload
    response = requests.post(webhook_url, json=data)

    #check if success
    if response.status_code == 204:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message: {response.status_code}')