import datetime
import requests
def get_covid_today():
    response = requests.get("https://covid19.th-stat.com/api/open/today")
    if response.status_code == 200:
        TodayDate = datetime.date.today()
        UpdateDate = response.json()["UpdateDate"]
        UpdateDate = datetime.datetime.strptime(UpdateDate[:10], "%d/%m/%Y").date()
        if UpdateDate == TodayDate:
            message = "\n"+"\n".join([f"{key}:{value}" for key, value in response.json().items()])
            return message
if __name__ == "main":
    message = get_covid_today()
    print(message)
