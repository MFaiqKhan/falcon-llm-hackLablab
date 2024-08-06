from deepgram import Deepgram
from flask import current_app

def transcribe_audio(audio_data: bytes):
    dg_client = Deepgram(current_app.config['DEEPGRAM_API_KEY'])
    source = {'buffer': audio_data, 'mimetype': 'audio/wav'}
    response = dg_client.transcription.sync_prerecorded(source, {'punctuate': True})
    return response['results']['channels'][0]['alternatives'][0]['transcript']

def text_to_speech(text: str):
    dg_client = Deepgram(current_app.config['DEEPGRAM_API_KEY'])
    response = dg_client.speak.sync(text)
    return response['audio']