import os
import google.generativeai as genai
import speech_recognition as sr
import requests
import json
import playsound
import google.cloud.texttospeech as tts

# Set API Key manually here (Replace with your actual API key)
GENAI_API_KEY = "API_KEY"

genai.configure(api_key=GENAI_API_KEY)


# Use the latest available Gemini model
gemini_model = genai.GenerativeModel("gemini-1.5-pro-latest")
#
# Configure Google Cloud TTS Client
tts_client = tts.TextToSpeechClient()

def text_to_speech(text):
    """Converts text to speech using Google Cloud TTS API and plays it."""
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-IN",  # Indian English
        name="en-IN-Chirp-HD-D",  # Choose a high-quality voice
        ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open("response.wav", "wb") as out:
        out.write(response.audio_content)

    # Play the generated speech
    playsound.playsound("response.wav")

# Initialize Speech Recognition
recognizer = sr.Recognizer()

def speech_to_text():
    """Continuously listens and converts speech to text."""
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            return text.strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Speech Recognition service unavailable."

def career_chatbot():
    """Continuous AI conversation for career guidance."""
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    career_field = input("Enter your desired career field: ")

    greeting = f"Hey {name}! I'm super excited to help you explore careers in {career_field}! Let's chat!"
    print(f"🤖 AI: {greeting}")
    text_to_speech(greeting)

    while True:
        user_input = speech_to_text()
        if not user_input:
            text_to_speech("Oops! I didn't catch that. Can you say it again?")
            continue

        if "exit" in user_input.lower():
            text_to_speech("Okay, have an amazing day ahead! Goodbye! ")
            break

        # Generate AI Response using Gemini
        response = gemini_model.generate_content(user_input)
        full_response = response.text.strip()

        # Generate a brief spoken summary
        summary_prompt = f"Summarize this in 2-3 sentences for speech output:\n{full_response}"
        summary_response = gemini_model.generate_content(summary_prompt)
        summary_text = summary_response.text.strip()

        # Display the full response on the screen
        print(f"\n🤖 AI (Full Response on Screen):\n{full_response}\n")

        # Speak only the summary
        text_to_speech(f"Here's a brief overview: {summary_text}. More details are on the screen!")

        # Ask follow-up question in a happy tone
        text_to_speech("Do you need to know anything else? I'm happy to help! ")

if __name__ == "__main__":
    career_chatbot()