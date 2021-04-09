import sys
import json
def load_token():
    with open("PythonLineNotify/tokens.json", "r") as file:
        data = json.load(file)
    return data

def save_token(data):
    with open("PythonLineNotify/tokens.json", "w") as file:
        json.dump(data, file)

def update_token(username, token):
    # Load json | Create new dict
    try:
        data = load_token()
    except FileNotFoundError:
        data = dict()

    # Create keys ["username", "token"] if no keys
    if not "username" in data.keys():
        data["username"] = []
    if not "token" in data.keys():
        data["token"] = []

    # Pop username and token if duplicate with the new one
    if username in data["username"]:
        index = data["username"].index(username)
        data["username"].pop(index)
        data["token"].pop(index)

    # Update
    data["username"].append(username)
    data["token"].append(token)

    # Save
    save_token(data)

if __name__=="__main__":
    # username, token (argv[1], argv[2])
    update_token(sys.argv[1], sys.argv[2])
