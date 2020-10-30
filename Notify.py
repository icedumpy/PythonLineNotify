import json
import requests
#%%
def load_json():
    with open("tokens.json", "r") as file:
        data = json.load(file)
    return data

def save_json(data):
    with open("tokens.json", "w") as file:
        json.dump(data, file)

def update_token(username, token):
    # Load json | Create new dict
    try:
        data = load_json()
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
    save_json(data)

def send_message(token, message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded',
               'Authorization':f'Bearer {token}'}
    requests.post(url=url, headers=headers, data={"message":message})    

def get_token(username):
    data = load_json()
    try:
        index = data["username"].index(username)
        token = data["token"][index]
        return token
    except KeyError:
        print("Invalid Username")
        return "Invalid username"

def main(username, message):
    token = get_token(username)
    send_message(token, message)
#%%
if __name__ == "__main__":
    main("Ice", "Hello World!")