from dotenv import load_dotenv
import requests
import json
import time
import os

load_dotenv()
api_url = os.getenv('API_URL')
api_token = os.getenv('API_TOKEN')
head = {"Content-Type":"application/x-www-form-urlencoded", "apikey":api_token, "Accept": "application/json"}

async def CheckStatus():
    try:
        response = requests.get(api_url + '/list', headers=head, timeout = 15).json()
        response = response[0]['status']
        response = {
            "status": 0,
            "res": '{res}'.format(res = response)
        }
    except Exception as e:
        response = {
            "status": 2,
            "res": '{e}'.format(e=e)
        }

    return json.dumps(response)

async def Stop():
    try:
        data = {'uuid': 'bd514e74-adeb-41ee-930a-8b5b4a57cfa9'}
        response = requests.post(api_url + '/stop', data = data, headers = head, timeout = 15).json()
        response = response['status']
        response = {
            "status": 0,
            "res": '{res}'.format(res = response)
        }
    except KeyError:
        response = {
            "status": 1,
            "res": "Cant get status from response."
        }
    except Exception as e:
        response = {
            "status": 2,
            "res": '{e}'.format(e=e)
        }
    return json.dumps(response)

async def Start():
    try:
        data = {'uuid': 'bd514e74-adeb-41ee-930a-8b5b4a57cfa9'}
        response = requests.post(api_url + '/start', data = data, headers = head, timeout = 15).json()
        response = response['status']
        response = {
            "status": 0,
            "res": '{res}'.format(res = response)
        }
    except KeyError:
        response = {
            "status": 1,
            "res": "Cant get status from response."
        }
    except Exception as e:
        response = {
            "status": 2,
            "res": '{e}'.format(e=e)
        }
    return json.dumps(response)