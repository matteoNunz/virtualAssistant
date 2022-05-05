import pyttsx3
import time
import speech_recognition as sr
from datetime import datetime
from random import choice
from utils import opening_text , available_lang
from State_machine import State_machine
from os_ops import open_calculator, open_camera, open_cmd, open_notepad , logout , take_photo
from online_ops import find_my_ip , get_location , search_on_wikipedia , play_on_youtube , search_on_google , \
    send_whatsapp_message , send_email , get_random_joke , get_random_advice , get_latest_news , get_weather_report , \
    get_translation


# Set the name of the user and of the assistant
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

# Set the starting state to the assistant
state_assistant = State_machine.WAITING

# Create a variable to keep in memory the time state LISTENING is activated, in order to disable it
#   if the user says nothing
start_listening_time = int(round(time.time() * 1000))

# Create a variable to keep in memory the time state COMPUTING is activated, in order to disable it
#   if the user says nothing
start_computing_time = int(round(time.time() * 1000))

# Save the time limit to deactivate the listening state (in seconds)
deactivate_listening_time = 8

# Create a variable to keep the starting time of the timer
starting_timer_time = int(round(time.time() * 1000))

# Create a variable to keep the timer duration required (in minutes)
timer_duration = 0

# Create a variable to keep if the timer is on or not
timer_on = False


def speak(text):
    """
    Used to speak whatever text is passed to it
    :param text: text to say
    """
    engine.say(text)
    engine.runAndWait()


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

    speak(f"I'm on!")


def listen(r):
    """
    Method used to listen what the user is saying (if he is saying something)
    :param r: is the recognizer
    :return: the audio object that could be converted
    """
    try:
        # Take the mic as source
        with sr.Microphone() as source:
            print('Listening....')
            # If the audio is greater than the threshold I'm saying something,
            #   otherwise it's just a long silence
            r.pause_threshold = 3
            # Listen the environment noise in order to reduce and correct it when
            #   listening the source (remove the noise)
            r.adjust_for_ambient_noise(source)
            # Take the audio object to convert in a string
            audio = r.listen(source=source , timeout=deactivate_listening_time)
    except sr.WaitTimeoutError as e:
        # If the time timeout is over, return
        return None

    print("End listening")
    return audio


def take_user_input():
    """
    Takes user input, recognizes it using Speech Recognition module and converts it into text
    """
    # Take the global variable
    global state_assistant
    global start_listening_time
    global start_computing_time
    global deactivate_listening_time

    # Initiate the recognizer
    r = sr.Recognizer()

    # If the state of the assistant is WAITING
    if state_assistant == State_machine.WAITING:
        print("Listening in waiting")
        # Listen the user
        audio = listen(r)

        try:
            # Convert the object audio in a string containing the phrase the user said
            query = r.recognize_google(audio, language='it-IT')

            # This is the command for the offline recognition, but it doesn't work
            # query = r.recognize_sphinx(audio , language= 'en-in')

            # If the user said the starting phrase
            print(query)
            if "okay" in query or "ok" in query:
                # Enable the interaction with the assistant
                print("Phrase recognized")
                speak("Ask me sir")
                # Change the state of the assistant in LISTENING
                state_assistant = State_machine.LISTENING
                # Set the init time of that phase (LISTENING)
                start_listening_time = int(round(time.time() * 1000))
                print("Going in listening")
        except Exception:
            # If the phrase is not recognize, do nothing
            # The phrase is not recognize also if there was silence
            query = ''
        return query

    # If the state of the assistant is LISTENING
    elif state_assistant == State_machine.LISTENING:
        # Listen what the user is saying
        audio = listen(r)

        # If the time is exceed (now - init time of the phase is bigger than the threshold)
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

            # If in the phrase there isn't 'stop'
            if 'stop' not in query:
                # Say a random phrase
                speak(choice(opening_text))
                # Change the state to COMPUTING
                state_assistant = State_machine.COMPUTING
                print("Going to computing")
            # Else if the user said 'stop', quit
            else:
                # Take the current hour
                hour = datetime.now().hour
                if (hour >= 21) or (hour < 6):
                    speak("Good night sir, take care!")
                else:
                    speak('Have a good day sir!')
                # End the application
                exit()
        except Exception:
            # If the assistant didn't recognize the phrase said
            speak('Sorry, I could not understand. Could you please say that again?')
            # Restart the initial phase time
            start_listening_time = int(round(time.time() * 1000))
            query = ''

        return query

    elif state_assistant == State_machine.COMPUTING:
        print("In take user input with state computing")
        # Listen what the user is saying
        audio = listen(r)

        # If the time is exceed (x 2 just because it could be longer)
        if int(round(time.time() * 1000)) - start_computing_time > deactivate_listening_time * 1000 * 2:
            # Came back to the WAITING state
            # print(int(round(time.time() * 1000)) - start_computing_time)
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
            # Re-initialize the starting computing phase time
            start_computing_time = int(round(time.time() * 1000))
            query = ''

        return query


def do_action(query):
    """
    Perform the action specified by the user
    :param query: is what the user said
    """
    # Take the global variables
    global state_assistant
    global start_listening_time
    global start_computing_time
    global starting_timer_time
    global timer_duration
    global timer_on

    # If the phase is not COMPUTING (nothing to execute), return
    if state_assistant != State_machine.COMPUTING:
        return

    # If the user said 'open notepad' or 'blocco note'
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
        # Update the starting computing time
        start_computing_time = int(round(time.time() * 1000))
        # Listen what the user is saying
        search_query = take_user_input().lower()
        print("Searching " + str(search_query))

        # If the user said nothing or something bad happened
        if len(search_query) == 0:
            speak("Sorry, I couldn't understand")
            return

        results = search_on_wikipedia(search_query)
        speak(f"According to Wikipedia, {results}")
        speak("For your convenience, I am printing it on the screen sir.")
        print(results)

    elif 'youtube' in query:
        speak('What do you want to play on Youtube, sir?')
        # Update the starting computing time
        start_computing_time = int(round(time.time() * 1000))
        video = take_user_input().lower()
        print("Searching " + str(video))

        # If the user said nothing or something bad happened
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
        speak('On what number should I send the message sir? Please enter in the console: ')
        number = input("Enter the number: ")
        speak("What is the message sir?")
        # Update the starting computing time
        start_computing_time = int(round(time.time() * 1000))
        message = take_user_input().lower()

        # If the user said nothing or something bad happened
        if len(message) == 0:
            speak("Sorry, I couldn't understand")
            return

        send_whatsapp_message(number, message)
        speak("I've sent the message sir.")

    # It works if you enable the access from less secure app in the google account
    elif "send an email" in query:
        speak("On what email address do I send sir? Please enter in the console: ")
        receiver_address = input("Enter email address: ")
        speak("What should be the subject sir?")
        # Update the starting computing time
        start_computing_time = int(round(time.time() * 1000))
        subject = take_user_input().capitalize()
        speak("What is the message sir?")
        # Update the starting computing time
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
        # Reduce the speed to better understand what the assistant is saying
        engine.setProperty('rate', 140)
        speak(get_latest_news())
        # Reset the correct speed
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

        # If the language is between the available ones
        if available_lang[from_lang] is not None:
            from_lang = available_lang[from_lang]
        else:
            speak("I didn't get it.")
            state_assistant = State_machine.LISTENING
            return

        speak("To which language?")
        start_computing_time = int(round(time.time() * 1000))
        to_lang = take_user_input().lower()

        # If the language is between the available ones
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

    elif 'what can you do' in query or 'cosa sai fare' in query:
        speak("I can open your apps, I can check the news or the weather for you, I can search for some topics"
              "on Wikipedia or on Google, I can also translate some phrases and, finally, I can make jokes")

    elif "log off" in query or "sign out" in query or 'logout' in query or 'disconnetti' in query:
        speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
        logout()

    elif "take a photo" in query or "scatta foto" in query:
        speak("Say cheseeeeeee!")
        take_photo()

    elif "set timer" in query or "imposta timer" in query:
        speak("Insert the duration in minutes")

        try:
            timer_duration = input()
            timer_duration = float(timer_duration)
            # Set the initial time
            starting_timer_time = time.localtime().tm_min
            # Set the timer is on
            timer_on = True
        except:
            speak("That's not a number")

    else:
        speak("Command not found! Repeat please")
        start_listening_time = int(round(time.time() * 1000))
        state_assistant = State_machine.LISTENING
        return

    # Command executed correctly
    # Turn back to WAITING state
    state_assistant = State_machine.WAITING
    print("Going to waiting")


if __name__ == '__main__':
    # Greeting the user
    greet_user()

    while True:
        # Interact with the user
        query = ''
        query = take_user_input().lower()
        print(state_assistant)
        print(query)
        # Perform the action required
        do_action(query)

        if timer_on:
            # Check if the timer is over
            if time.localtime().tm_min - starting_timer_time > timer_duration:
                # Increase the volume for the alarm message
                engine.setProperty('volume', 4.0)
                speak("Time is up!.")
                time.sleep(0.5)
                speak("Time is up!.")
                time.sleep(0.1)
                speak("Time is up!.")
                engine.setProperty('volume', 1.0)
                # Deactivate the timer on flag
                timer_on = False


