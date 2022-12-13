import json
import os

def CreateNewFile(inName):
    try:
        os.makedirs(os.path.dirname("data/{name}".format(name = inName)), exist_ok=True)
        open("data/{name}".format(name = inName), "w")
        WriteFile([], inName)
        return True
    except Exception as e:
        print(e)
        return False

def ReadFile(inName):
    os.makedirs(os.path.dirname("data/{name}".format(name = inName)), exist_ok=True)
    with open("data/{name}".format(name = inName), 'r') as read_file:
        return json.load(read_file)

def WriteFile(data, inName):
    try:
        os.makedirs(os.path.dirname("data/{name}".format(name = inName)), exist_ok=True)
        with open("data/{name}".format(name = inName), 'w') as write_file:
            json.dump(data, write_file, indent=4, separators=(',',': '))
            return True
    except Exception as e:
        print(e)
        return False

def DeserializationJson(inName):
    try:
        return ReadFile("{name}.json".format(name = inName))
    except FileNotFoundError:
        CreateNewFile("{name}.json".format(name = inName))
        return ReadFile("{name}.json".format(name = inName))
    except Exception as e:
        print(e)
        return False

def SerializationJson(data, inName):
    try:
        return WriteFile(data, "{name}.json".format(name = inName))
    except FileNotFoundError:
        CreateNewFile("{name}.json".format(name = inName))
        return WriteFile(data, "{name}.json".format(name = inName))
    except Exception as e:
        print(e)
        return False