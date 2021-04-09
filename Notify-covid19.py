import sys
from functions import get_covid_today, send_message

if __name__ == "__main__":
    status, message = get_covid_today()
    if status:
        username = sys.argv[1]
        send_message(username, message)