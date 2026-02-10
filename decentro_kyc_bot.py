import speech_recognition as sr
import pyttsx3
import json
import re
from datetime import datetime

engine = pyttsx3.init()

def speak(text):
    print("BOT:", text)
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("YOU:", text)
        return text.lower().strip()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def ask_with_retry(prompt, validate_fn, error_msg):
    attempts = 0
    while attempts < 3:   # first try + 2 retries
        speak(prompt)
        user_input = listen()

        if validate_fn(user_input):
            return user_input

        attempts += 1
        if attempts < 3:
            speak(error_msg)

    speak("Sorry, we could not verify this information. Please try again later.")
    exit(0)

def validate_name(name):
    return len(name.strip()) > 0

def validate_phone(phone):
    digits = re.sub(r"\D", "", phone)
    return len(digits) == 10

def extract_phone(phone):
    return re.sub(r"\D", "", phone)

def validate_pan(pan):
    pan = pan.replace(" ", "")
    return re.fullmatch(r"[a-zA-Z0-9]{10}", pan) is not None

def validate_consent(text):
    return "yes" in text or "no" in text

def extract_consent(text):
    return "yes" in text

def main():

    speak("Welcome to Decentro KYC verification.")

    name = ask_with_retry(
        "May I have your full name?",
        validate_name,
        "Sorry, I did not get your name. Please say your full name again."
    )

    phone_raw = ask_with_retry(
        "Please say your ten digit phone number.",
        validate_phone,
        "The phone number seems invalid. Please say a ten digit phone number."
    )
    phone = extract_phone(phone_raw)

    pan = ask_with_retry(
        "Please say your PAN number.",
        validate_pan,
        "The PAN number seems invalid. Please say your ten character PAN number again."
    )
    pan = pan.replace(" ", "").upper()

    consent_text = ask_with_retry(
        "Do you consent to verification? Please say yes or no.",
        validate_consent,
        "Please clearly say yes or no."
    )
    consent = extract_consent(consent_text)

    speak(f"Confirming your details. Name {name}. Phone number {phone}. PAN {pan}.")

    if not consent:
        speak("You have not given consent. The verification cannot be completed.")
        exit(0)

    session_data = {
        "name": name,
        "phone": phone,
        "pan": pan,
        "consent": consent,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open("kyc_session.json", "w") as f:
        json.dump(session_data, f, indent=4)

    speak("Your KYC verification is completed successfully. Thank you for using Decentro.")

if __name__ == "__main__":
    main()
