import datetime
import webbrowser

import pyttsx3
import speech_recognition as sr

recognizer = sr.Recognizer()


def speak(text):
    """Print the text and say it out loud."""
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen from microphone. Return text, or None if not understood."""
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return None
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please repeat.")
    except sr.RequestError:
        speak("Cannot reach the speech service. Check your internet.")
    return None


def handle_command(command):
    """Act on the command. Return False to quit."""
    words = command.split()

    if "hello" in words or "hi" in words:
        speak("Hello! How can I help you?")

    elif "time" in words:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in words or "day" in words:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "search" in words:
        query = command.split("search", 1)[1].strip()
        if query.startswith("for "):
            query = query[4:]
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")

    elif "stop" in words or "exit" in words or "bye" in words:
        speak("Goodbye!")
        return False

    else:
        speak("I can tell the time, the date, search the web, or say hello.")
    return True


def main():
    speak("Voice assistant ready. Say hello, ask the time, or say search followed by a topic.")
    running = True
    while running:
        command = listen()
        if command:
            running = handle_command(command)


if __name__ == "__main__":
    main()