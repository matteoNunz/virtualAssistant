import requests
import socket
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import translators as ts
import smtplib

import geocoder
import folium

NEWS_API_KEY = "f74e553ce2aa42e29029f1e2043b147b"
OPEN_WEATHER_APP_ID = "d425c0fbf463e60f7f9c98a052693815"

EMAIL = "MAIL"
PASSWORD = "PASSWORD"

# Set the language. The default is en
wikipedia.set_lang('it')


def find_my_ip():
    # To get the IPv6
    ip_address_6 = requests.get('https://api64.ipify.org?format=json').json()

    # Getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    # Getting the IP address using socket.gethostbyname() method
    ip_address_4 = socket.gethostbyname(hostname)

    return ip_address_6["ip"] , ip_address_4


def get_location():
    # Get the coordinates
    g = geocoder.ip("me")
    my_address = g.latlng

    my_map = folium.Map(location = my_address,
                        zoom_start = 12)

    folium.CircleMarker(location = my_address,
                        radius = 50,
                        popup = "Milan").add_to(my_map)

    folium.Marker(my_address,
                  popup = "Milan").add_to(my_map)

    my_map.save("my_map.html")

    return g , my_address


def search_on_wikipedia(query):
    # Search on wikipedia what the user said. Take just the first sentence
    results = wikipedia.summary(f'{query}', sentences=2)
    return results


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+39{number}", message)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=it&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_APP_ID}&units=metric").json()

    print(res)

    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


def get_translation(phrase , from_lang , to_lang):

    translation = ts.google(phrase, from_language=from_lang, to_language=to_lang)
    return translation

