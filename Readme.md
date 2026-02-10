# Decentro Voice KYC Bot

This project is a simple Python command-line voice bot that simulates a KYC verification call for a fintech onboarding flow.

## Features

- Voice based interaction using microphone
- Collects name, phone number, PAN and consent
- Performs basic validations
- Speaks prompts and confirmations
- Saves session details as JSON

## Setup

Install dependencies:

pip install SpeechRecognition pyttsx3
pip install pipwin
pipwin install pyaudio

## Run

python decentro_kyc_bot.py

## Output

A sample JSON file will be created as:

kyc_session.json
