from functions import get_token, send_message

if __name__ == "__main__":
    token = get_token("Ice")
    send_message(token, "Hello World")