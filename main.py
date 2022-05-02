#####

# Add the alarm

"""
To switch off the pc
        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
"""
#####

import pyttsx3
import time
import speech_recognition as sr
from datetime import datetime
from random import choice
from utils import opening_text , available_lang
from State_machine import State_machine
from os_ops import open_calculator, open_camera, open_cmd, open_notepad
from online_ops import find_my_ip , get_location , search_on_wikipedia , play_on_youtube , search_on_google , \
    send_whatsapp_message , send_email , get_random_joke , get_random_advice , get_latest_news , get_weather_report , \
    get_translation
from pprint import pprint

import ecapture

USERNAME = "Matteo"
BOT_NAME = "Tech-girl"

# Sapi5 is a Microsoft Text to speech engine used for voice recognition
engine = pyttsx3.init('sapi5')

# Set Rate: speed of reproduction
engine.setProperty('rate', 200)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set the starting state of the assistant
state_assistant = State_machine.WAITING

# Create a variable to keep in memory the time state LISTENING is activated, in order to disable it
#   if the user says nothing
start_listening_time = int(round(time.time() * 1000))

# Create a variable to keep in memory the time state COMPUTING is activated, in order to disable it
#   if the user says nothing
start_computing_time = int(round(time.time() * 1000))

# Save the time limit to deactivate the listening state
deactivate_listening_time = 8


def speak(text):
    """
    Used to speak whatever text is passed to it
    :param text: text to say
    """
    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """
    Greets the user according to the time
    """
    hour = datetime.now().hour
    if (hour >= 5) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 23):
        speak(f"Good Evening {USERNAME}")
    else:
        speak(f"It's late {USERNAME}, you should rest")

    speak(f"I am {BOT_NAME}. I'm on!")


# Listen what the user is saying
def listen(r):
    # Take the mic as source
    with sr.Microphone() as source:
        print('Listening....')
        # If the audio is greater than the threshold I'm saying something,
        # otherwise it's just a long silence
        r.pause_threshold = 3
        # Take the audio object to convert in a string
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source=source , timeout=deactivate_listening_time)

    print("End listening")
    return audio


# Takes Input from User
def take_user_input():
    """
    Takes user input, recognizes it using Speech Recognition module and converts it into text
    """
    # Consider the global variable
    global state_assistant
    global start_listening_time
    global start_computing_time
    global deactivate_listening_time

    # Initiate the recognizer
    r = sr.Recognizer()

    if state_assistant == State_machine.WAITING:
        print("Listening in waiting")
        audio = listen(r)

        try:
            # Recognize the phrase
            query = r.recognize_google(audio, language='it-IT')

            # This is the command for the offline recognition, but it doesn't work
            # query = r.recognize_sphinx(audio , language= 'en-in')

            # If the user said the starting phrase
            print(query)
            if "okay" in query or "ok" in query:
                # Enable the interaction with the assistant
                print("Phrase recognized")
                speak("Ask me sir")
                state_assistant = State_machine.LISTENING
                start_listening_time = int(round(time.time() * 1000))
                print("Going in listening")
        except Exception:
            query = ''
        return query

    elif state_assistant == State_machine.LISTENING:
        # Listen what the user is saying
        audio = listen(r)

        # If the time is exceed
        if int(round(time.time() * 1000)) - start_listening_time > deactivate_listening_time * 1000:
            # Came back to the WAITING state
            state_assistant = State_machine.WAITING
            print("Going to waiting")
            return ''

        # If the assistant listens something

        try:
            print(audio)
            print('Recognizing...')
            # Recognize the phrase
            query = r.recognize_google(audio, language='it-IT')

            # If in the phrase there aren't 'exit' or 'stop', quit
            if 'stop' not in query:
                speak(choice(opening_text))
                # Change the state to COMPUTING
                state_assistant = State_machine.COMPUTING
                print("Going to computing")
            else:
                hour = datetime.now().hour
                if (hour >= 21) or (hour < 6):
                    speak("Good night sir, take care!")
                else:
                    speak('Have a good day sir!')
                # End the application
                exit()
        except Exception:
            speak('Sorry, I could not understand. Could you please say that again?')
            query = ''

        return query

    elif state_assistant == State_machine.COMPUTING:
        print("In take user input with state computing")
        audio = listen(r)

        # If the time is exceed (x 2 just because it could be longer)
        if int(round(time.time() * 1000)) - start_computing_time > deactivate_listening_time * 1000 * 2:
            # Came back to the WAITING state
            print(int(round(time.time() * 1000)) - start_computing_time)
            state_assistant = State_machine.WAITING
            print("Going to waiting")
            return ''

        # If the assistant listens something

        try:
            print(audio)
            print('Recognizing...')
            # Recognize the phrase
            query = r.recognize_google(audio, language='it-IT')

        except Exception:
            speak('Sorry, I could not understand. Could you please say that again?')
            query = ''

        return query


def do_action(query):
    """
    Perform the action specified by the user
    :param query: is what the user said
    """
    global state_assistant
    global start_computing_time

    # If there is nothing to execute, exit
    if state_assistant != State_machine.COMPUTING:
        return

    if 'open notepad' in query or 'blocco note' in query:
        open_notepad()

    elif 'open command prompt' in query or 'open cmd' in query or 'cmd' in query or 'terminale' in query:
        open_cmd()

    elif 'open calculator' in query or 'calcolatrice' in query:
        open_calculator()

    elif 'open camera' in query or 'camera' in query or 'fotocamera' in query:
        open_camera()

    elif 'ip address' in query or 'indirizzo ip' in query:
        ip_v6 , ip_v4 = find_my_ip()
        # Reduce the speed to better understand the ip
        engine.setProperty('rate', 150)
        speak(f'Your ip_v4 is {ip_v4}\n For your convenience, I am printing it on the screen sir.')
        print("Your ip_v4 is: " + str(ip_v4))
        print("Your ip_v6 is: " + str(ip_v6))
        # Increase again the speed
        engine.setProperty('rate', 200)

    elif 'location' in query or 'my location' in query or 'posizione' in query:
        coordinates , city = get_location()
        speak("I'm printing your coordinates and your city on the screen sir")
        print(f'Your coordinates are {coordinates}')
        print(f'Your city is {city}')

    elif 'wikipedia' in query:
        speak('What do you want to search on Wikipedia, sir?')
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        search_query = take_user_input().lower()
        print("Searching " + str(search_query))

        if len(search_query) == 0:
            speak("Sorry, I couldn't understand")
            return

        state_assistant = State_machine.WAITING
        results = search_on_wikipedia(search_query)
        speak(f"According to Wikipedia, {results}")
        speak("For your convenience, I am printing it on the screen sir.")
        print(results)

    elif 'youtube' in query:
        speak('What do you want to play on Youtube, sir?')
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        video = take_user_input().lower()
        print("Searching " + str(video))
        if len(video) == 0:
            speak("Sorry, I couldn't understand")
            return
        play_on_youtube(video)

    elif 'search on google' in query:
        speak('What do you want to search on Google, sir?')
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        search_query = take_user_input().lower()
        search_on_google(search_query)

    elif "send whatsapp message" in query:
        speak(
            'On what number should I send the message sir? Please enter in the console: ')
        number = input("Enter the number: ")
        speak("What is the message sir?")
        message = take_user_input().lower()
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        send_whatsapp_message(number, message)
        speak("I've sent the message sir.")

    # It works if you enable the access from less secure app in the google account
    elif "send an email" in query:
        speak("On what email address do I send sir? Please enter in the console: ")
        receiver_address = input("Enter email address: ")
        speak("What should be the subject sir?")
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        subject = take_user_input().capitalize()
        speak("What is the message sir?")
        # Update the starting listening time
        start_computing_time = int(round(time.time() * 1000))
        message = take_user_input().capitalize()
        if send_email(receiver_address, subject, message):
            speak("I've sent the email sir.")
        else:
            speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

    elif 'joke' in query or 'scherzo' in query:
        speak(f"Hope you like this one sir")
        joke = get_random_joke()
        speak(joke)
        speak("For your convenience, I am printing it on the screen sir.")
        print(joke)

    elif "advice" in query or 'consiglio' in query:
        speak(f"Here's an advice for you, sir")
        advice = get_random_advice()
        speak(advice)
        speak("For your convenience, I am printing it on the screen sir.")
        print(advice)

    elif 'news' in query or 'notizia' in query or 'notizie' in query:
        speak(f"I'm reading out the latest news headlines, sir")
        engine.setProperty('rate', 140)
        speak(get_latest_news())
        engine.setProperty('rate', 200)
        speak("For your convenience, I am printing it on the screen sir.")
        print(*get_latest_news(), sep='\n')

    elif 'weather' in query or 'meteo' in query:
        speak("For which city?")
        start_computing_time = int(round(time.time() * 1000))
        city = take_user_input().lower()

        speak(f"Getting weather report for {city}")
        weather, temperature, feels_like = get_weather_report(city)
        engine.setProperty('rate', 150)
        speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
        speak(f"Also, the weather report talks about {weather}")
        engine.setProperty('rate', 200)
        speak("For your convenience, I am printing it on the screen sir.")
        print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

    elif 'translate' in query or 'translator' in query or 'traduttore' in query or 'traduci' in query:
        speak("From which language?")
        start_computing_time = int(round(time.time() * 1000))
        from_lang = take_user_input().lower()

        if available_lang[from_lang] is not None:
            from_lang = available_lang[from_lang]
        else:
            speak("I didn't get it.")
            state_assistant = State_machine.LISTENING
            return

        speak("To which language?")
        start_computing_time = int(round(time.time() * 1000))
        to_lang = take_user_input().lower()

        if available_lang[to_lang] is not None:
            to_lang = available_lang[to_lang]
        else:
            speak("I didn't get it.")
            state_assistant = State_machine.LISTENING
            return

        speak("Which is the phrase?")
        phrase = take_user_input().lower()

        translation = get_translation(phrase , from_lang , to_lang)
        speak(f"The translation is {translation}")
        print(f"The translation is {translation}")

    elif 'who are you' in query or 'your name' in query or 'chi sei' in query or 'tuo nome' in query:
        speak("I'm Tech-girl, your personal assistant.\n"
              " Tell me if you need something and I'll try to do it for you")
        state_assistant = State_machine.LISTENING

    elif 'what can you do' in query or 'cosa sai fare' in query:
        speak("I can open your apps, I can check the news or the weather for you, I can search for some topics"
              "on Wikipedia or on Google, I can also translate some phrases and, finally, I can make jokes")
        state_assistant = State_machine.LISTENING

    else:
        speak("Command not found! Repeat please")
        state_assistant = State_machine.LISTENING
        return

    # Command executed correctly
    state_assistant = State_machine.WAITING
    print("Going to waiting")


if __name__ == '__main__':
    greet_user()

    while True:
        # Interact with the user
        query = ''
        query = take_user_input().lower()
        print(state_assistant)
        print(query)
        # Perform the action required
        do_action(query)

