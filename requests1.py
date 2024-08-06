import requests
import json
import base64
import pyaudio
import wave
import io

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

# Server configuration
SERVER_URL = "http://127.0.0.1:3030/api"

def text_chat(query):
    url = f"{SERVER_URL}/chat/text"
    headers = {"Content-Type": "application/json"}
    data = {"query": query}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=100)
        response.raise_for_status()
        result = response.json()
        print("------result---",result)
        print(f"Query: {result['query']}")
        print(f"Response: {result['response']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to connect to the server. Make sure it's running on {SERVER_URL}")
        print(f"Details: {str(e)}")

def audio_chat():
    url = f"{SERVER_URL}/chat/audio"
    headers = {"Content-Type": "application/octet-stream"}

    audio_data = record_audio()
    try:
        response = requests.post(url, headers=headers, data=audio_data, timeout=10)
        response.raise_for_status()
        result = response.json()
        print(f"Transcribed Query: {result['query']}")
        print(f"Response: {result['response']}")
        
        # Decode and play audio response
        audio_response = base64.b64decode(result['audio_response'].encode('latin-1'))
        play_audio(audio_response)
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to connect to the server. Make sure it's running on {SERVER_URL}")
        print(f"Details: {str(e)}")

def main():
    print(f"Connecting to server at {SERVER_URL}")
    while True:
        print("\n1. Text Chat")
        print("2. Audio Chat")
        print("3. Quit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            query = input("Enter your text query: ")
            text_chat(query)
        elif choice == '2':
            audio_chat()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()