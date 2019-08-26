import json


def stdin_extractor():
    print("Paste the json content. Blank line to save it.")
    content = ""
    while True:
        line = input()
        if line == "":
            break
        content += line
    return json.loads(content)


def file_extractor(path):
    with open(path) as file:
        return json.loads(file.read())
