import requests
from twilio.rest import Client




def check_rain():
    parameters = {
        "lat": 50.99,
        "lon": 22.14,
        "exclude": "minutely,daily",
        "appid": os.environ("appid"),
    }

    response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
    response.raise_for_status()
    data = response.json()
    rain = False

    for x in data["hourly"][:12]:
        if x["weather"][0]["id"] < 700:
            rain = True
    return rain


account_sid = os.environ("account_sid")
auth_token = os.environ("auth_token")
if check_rain():
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an Umbrella.",
        from_=os.environ("twilionumber"),
        to=os.environ("mynumber")
    )
    print(message.status)