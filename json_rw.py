import json

def writeJSON(path, name, data):
    file_path = path + '/' + name
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def getJSON(path, name):
    file_path = path + '/' + name
    with open(file_path, "r") as json_file :
        json_data = json.load(json_file)
        return json_data

