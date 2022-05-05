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

# Set the language of Wikipedia. The default is en
wikipedia.set_lang('it')


def find_my_ip():
    """
    Method that find the ipv6 and the ipv4 of your machine
    :return: ipv6 address , ipv4 address
    """
    # To get the IPv6 make a request to a site and convert the output in json format
    ip_address_6 = requests.get('https://api64.ipify.org?format=json').json()

    # Getting the hostname
    hostname = socket.gethostname()
    # Getting the IPv4 address
    ip_address_4 = socket.gethostbyname(hostname)

    return ip_address_6["ip"] , ip_address_4


def get_location():
    """
    Method that given the current ip find your approximate position
    :return: the coordinates and the city
    """
    # Get the coordinates. 'me' is the current ipv4
    g = geocoder.ip("me")
    # from g take latitude and longitude
    my_address = g.latlng

    # Shoe the location found in the map
    my_map = folium.Map(location = my_address,
                        zoom_start = 12)

    # Add a circle in the corresponding location
    folium.CircleMarker(location = my_address,
                        radius = 50,
                        popup = "Milan").add_to(my_map)

    # Add a marker in the circle
    folium.Marker(my_address,
                  popup = "Milan").add_to(my_map)

    # Save the map file as an html
    my_map.save("my_map.html")

    return g , my_address


def search_on_wikipedia(query):
    """
    Method that search something on Wikipedia
    :param query: is the input, what to search
    :return: the first 2 sentences returned by Wikipedia
    """
    # Search on wikipedia what the user said. Take just the first sentence
    results = wikipedia.summary(f'{query}', sentences=2)
    return results


def play_on_youtube(video):
    """
    Method that open YouTube searching the video corresponding to the input
    :param video: is the video to look for
    :return: nothing
    """
    kit.playonyt(video)


def search_on_google(query):
    """
    Method that open Google searching the topic corresponding to the input
    :param query: is the topic to look for
    :return: nothing
    """
    kit.search(query)


def send_whatsapp_message(number, message):
    """
    Method that open WhatsApp Web and send a message
    :param number: is the number to which send the message
    :param message: is the body of the message
    :return: nothing
    """
    kit.sendwhatmsg_instantly(f"+39{number}", message)


def send_email(receiver_address, subject, message):
    """
    Method used to send an email.
    Important: to work it's necessary to enable the "access from non secure sources"
    :param receiver_address: is the receiver address
    :param subject: is the object of the main
    :param message: is the body of the mail
    :return: nothing
    """
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
    """
    Method used to get a random joke making a request to a website
    :return: the string with the joke
    """
    # Prepare the header of the request
    headers = {
        'Accept': 'application/json'
    }
    # Make the request and put the result in the json format
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    """
    Method used to get a random advice making a request to a web site
    :return: the string with the advice
    """
    # Make the request
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def get_latest_news():
    """
    Method used to get the popular news in a given country -> country = it, category = general
    :return: the first 5 news returned by the website
    """
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=it&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city):
    """
    Method used to retrieve the weather in a given city
    :param city: is the city of which weather is required
    :return: the weather, the temperature and the feels like temperature
    """
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_APP_ID}&units=metric").json()

    # Access the wanted values from res
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


def get_translation(phrase , from_lang , to_lang):
    """
    Method used to make translations
    :param phrase: is the phrase to translate
    :param from_lang: is the language of the phrase
    :param to_lang: is the language of the output phrase
    :return: the original phrase translated in to_lang
    """
    translation = ts.google(phrase, from_language=from_lang, to_language=to_lang)
    return translation

