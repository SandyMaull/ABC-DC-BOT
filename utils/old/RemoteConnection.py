import os
import time
import json
import paramiko
from dotenv import load_dotenv

load_dotenv()
Host = os.getenv("SSH_HOST")
User = os.getenv("SSH_USER")
Pass = os.getenv('SSH_PASS')
Port = int(os.getenv('SSH_PORT'))

def run_command(command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(Host, port=Port, username=User, password=Pass, timeout=5)
        (stdin, stdout, stderr) = client.exec_command(command)
        cmd_output = stdout.read()
        response = {
            "status": 0,
            "res": cmd_output
        }
    except Exception as e:
        response = {
            "status": 1,
            "res": '{e}'.format(e = e)
        }
    finally:
        client.close()
    return response
 
def status():
    data = run_command("sudo service kuromine1 status")
    if data['status'] == 1:
        return data

    data = data["res"].decode("utf-8")
    data = data.split('\n')[2]
    data = data.split(':')[1]
    data = data.split()[0]
    data = {
        "status": 0,
        "res": data
        }
    return data

def start():
    data = status()
    if data["status"] == 0 and data["res"] == 'active':
        response = {
            "status": 0,
            "res": '{r}'.format(r = data)
        }
    elif data["status"] == 0:
        try:
            data = run_command("sudo service kuromine1 start")
            time.sleep(2)
            data = status()
            if data["status"] == 0:
                response = {
                    "status": 0,
                    "res": '{r}'.format(r = data)
                }
            else:
                response = {
                    "status": 2,
                    "res": '{r}'.format(r = data["res"])
                }
        except Exception as e:
            response = {
                "status": 1,
                "res": '{e}'.format(e = e)
            }
    else:
        response = data
    return json.dumps(response)

def stop():
    data = status()
    if data["status"] == 0 and data["res"] != 'active':
        response = {
            "status": 0,
            "res": '{r}'.format(r = data)
        }
    elif data["status"] == 0:
        try:
            data = run_command("sudo service kuromine1 stop")
            time.sleep(2)
            data = status()
            if data["status"] == 0:
                response = {
                    "status": 0,
                    "res": '{r}'.format(r = data)
                }
            else:
                response = {
                    "status": 2,
                    "res": '{r}'.format(r = data["res"])
                }
        except Exception as e:
            response = {
                "status": 1,
                "res": '{e}'.format(e = e)
            }
    else:
        response = data
    return json.dumps(response)