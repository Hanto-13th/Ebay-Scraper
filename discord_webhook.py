import requests
import os
from dotenv import load_dotenv

#load the .env
load_dotenv()

def send_the_data(message_to_send):
    """This function send the complete analyzed from user requests into a user discord server using webhook.
    It takes in argument: the complete analyzed data to post"""
    
    #get the URL from the .env
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    for part_of_msg in message_to_send:

        #load the content of message and bot settings (Formated in JSON)
        data = {
        'content': f'{part_of_msg}',
        'username': 'Log Scraper',
        'flags': 4
            }
        #post the request using URl and payload
        response = requests.post(webhook_url, json=data)

        #check if success
        if response.status_code == 204:
            print('Message sent successfully!')
        else:
            print(f'Failed to send message: {response.status_code}')
            print(response.text)

def render_message(all_the_message):
    CHAR_NUMBER = 50
    return f"NEW LOG:\n\n{all_the_message}" + CHAR_NUMBER * "#"




def truncate_the_longest_msg(all_the_message):
    MAX_CHAR = 2000
    return [all_the_message[i:i+MAX_CHAR] for i in range(0, len(all_the_message), MAX_CHAR)]



