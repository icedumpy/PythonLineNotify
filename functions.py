import os
import json
import datetime
import requests

def load_json(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data

def save_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file)

def load_token():
    data = load_json("tokens.json")
    return data

def save_token(data):
    save_json("tokens.json", data)

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

def show_tokens():
    data = load_token()
    for username, token in zip(data["username"], data["token"]):
        print(f"{username}: {token}")

def send_message(username, message):
    token=get_token(username)
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded',
               'Authorization':f'Bearer {token}'}
    requests.post(url=url, headers=headers, data={"message":message})

def get_token(username):
    data = load_token()
    try:
        index = data["username"].index(username)
        token = data["token"][index]
        return token
    except KeyError:
        print("Invalid Username")
        return "Invalid username"

def get_covid_today():
    os.makedirs("Covid-stats", exist_ok=True)
    TodayDate = datetime.date.today()
    if not os.path.exists(os.path.join("Covid-stats", str(TodayDate)+".json")):
        response = requests.get("https://covid19.th-stat.com/api/open/today")
        if response.status_code == 200:
            UpdateDate = response.json()["UpdateDate"]
            UpdateDate = datetime.datetime.strptime(UpdateDate[:10], "%d/%m/%Y").date()
            if UpdateDate == TodayDate:
                message = f"\n{UpdateDate.strftime('%d')} {UpdateDate.strftime('%B')} {UpdateDate.strftime('%Y')}\n\n"+"\n".join([f"{key}: {int(value):,}" if key not in ["UpdateDate", "Source", "DevBy", "SeverBy"] else f"{key}: {value}" for key, value in response.json().items()])
                save_json(os.path.join("Covid-stats", str(TodayDate)+".json"), response.json())
                return True, message
            else:
                return False, ""
    else:
        return False, ""