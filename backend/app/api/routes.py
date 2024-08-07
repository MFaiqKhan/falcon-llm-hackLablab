from flask import request, jsonify, Blueprint
from ..services import falcon_service
#from ..audio_recorder import record_audio_with_vad
#from .speech_to_text import transcribe_audio
#from .text_to_speech import synthesize_audio
#from .audio_player import play_audio_stream
import pyaudio
import webrtcvad
from deepgram import DeepgramClient, PrerecordedOptions
import io
import time
import os
import requests
import time
import sounddevice as sd
import soundfile as sf

api_bp = Blueprint('api', __name__)


DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(DEEPGRAM_API_KEY)

DEEPGRAM_URL = 'https://api.deepgram.com/v1/speak?model=aura-stella-en'

def synthesize_audio(text):
    """
    Synthesize text to speech using Deepgram API.
    Args:
    text (str): The text to be converted to speech.
    Returns:
    bytes: Raw audio data if successful, None otherwise.
    Raises:
    requests.RequestException: If there's an error in the API request.
    """
    start_time = time.time()
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    
    try:
        with requests.post(DEEPGRAM_URL, headers=headers, json=payload) as r:
            r.raise_for_status()
            end_time = time.time()
            print(f"Synthesizing Audio: {(end_time - start_time) * 1000} ms")
            return r.content
    except requests.RequestException as e:
        print(f"Error in synthesize_audio: {str(e)}")
        return None



def play_audio_stream(audio_data):
    """
    Play audio from byte data.
    Args:
    audio_data (bytes): Raw audio data to be played.
    Returns:
    None
    Raises:
    Exception: If there's an error playing the audio.
    """
    if audio_data is not None:
        try:
            audio_io = io.BytesIO(audio_data)
            with sf.SoundFile(audio_io) as sound_file:
                samplerate = sound_file.samplerate
                data = sound_file.read()
                sd.play(data, samplerate)
                sd.wait()
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
    else:
        print("No audio data to play.")

def transcribe_audio(audio_data):
    """
    Transcribe audio data to text using Deepgram API.
    Args:
    audio_data (bytes): Raw audio data to be transcribed.
    Returns:
    str: Transcribed text if successful, empty string otherwise.
    Raises:
    Exception: If there's an error during transcription.
    """
    print("Received audio data length:", len(audio_data))
    start_time = time.time()
    
    if audio_data is None:
        return ""
    
    source = {'buffer': io.BytesIO(audio_data), 'mimetype': 'audio/webm'}
    options = PrerecordedOptions(model="nova-2", smart_format=True, language="en")
    
    try:
        response = deepgram.listen.rest.v("1").transcribe_file(source, options)
        print("Deepgram response:", response)
        end_time = time.time()
        print(f"Transcribe time: {(end_time - start_time) * 1000} ms")
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception as e:
        print(f"Error in transcribe_audio: {str(e)}")
        return ""

# You might want to import these from a central config file
CHUNK = 240
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
VAD_MODE = 3
SILENCE_THRESHOLD = 15

def record_audio_with_vad():
    """
    Record audio using Voice Activity Detection (VAD).
    Returns:
    bytes: Raw audio data if speech is detected, None otherwise.
    The function will continue recording until it detects a significant pause in speech.
    """
    p = pyaudio.PyAudio()
    vad = webrtcvad.Vad(VAD_MODE)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Listening... (Speak now)")
    frames = []
    silent_chunks = 0
    voice_detected = False
    
    while True:
        data = stream.read(CHUNK)
        is_speech = vad.is_speech(data, RATE)

        if is_speech:
            silent_chunks = 0
            voice_detected = True
        elif voice_detected:
            silent_chunks += 1

        if voice_detected:
            frames.append(data)

        if silent_chunks > SILENCE_THRESHOLD and voice_detected:
            break

    print("Done recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    if not frames:
        print("No speech detected.")
        return None
    
    return b''.join(frames)

@api_bp.route('/chat/audio', methods=['POST'])
def audio_chat():
    # Record audio
    audio_data = record_audio_with_vad()
    if not audio_data:
        return jsonify({"error": "No speech detected"}), 400
    
    # Transcribe audio to text
    query = transcribe_audio(audio_data)
    if not query:
        return jsonify({"error": "Failed to transcribe audio"}), 500
    
    # Process query using Falcon LLM with integrated RAG
    response = falcon_service.process_query(query)
    
    # Synthesize response to speech
    audio_response = synthesize_audio(response)
    if not audio_response:
        return jsonify({"error": "Failed to synthesize audio response"}), 500
    
    # Play audio response (you might want to handle this on the client-side instead)
    play_audio_stream(audio_response)
    
    return jsonify({
        "query": query,
        "response": response,
        "audio_response": audio_response.decode('latin-1')  # Convert bytes to string for JSON serialization
    })

@api_bp.route('/chat/text', methods=['POST'])
def text_chat():
    data = request.json
    print("data-----", data)
    query = data.get('query')
    print("query-----", query)
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Process query using Falcon LLM with integrated RAG
    response = falcon_service.process_query(query)
    print("response----", response)
    
    return jsonify({
        "query": query,
        "response": response
    })

""" from flask import request, jsonify
from . import api_bp
from ..services import deepgram_service, rag_service, medical_ner_service, drug_interaction_service, symptom_checker_service, medical_literature_service

@api_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        audio_data = file.read()
        transcript = deepgram_service.transcribe_audio(audio_data)
        return jsonify({"transcript": transcript})

@api_bp.route('/process', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    response = rag_service.process_query(query)
    entities = medical_ner_service.recognize_medical_entities(response)
    return jsonify({"response": response, "entities": entities})

@api_bp.route('/speak', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    audio = deepgram_service.text_to_speech(text)
    return jsonify({"audio": audio})

@api_bp.route('/check_interactions', methods=['POST'])
def check_interactions():
    data = request.json
    drugs = data.get('drugs')
    if not drugs:
        return jsonify({"error": "No drugs provided"}), 400
    result = drug_interaction_service.check_drug_interactions(drugs)
    return jsonify({"result": result})

@api_bp.route('/analyze_symptoms', methods=['POST'])
def analyze_symptoms():
    data = request.json
    symptoms = data.get('symptoms')
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400
    result = symptom_checker_service.analyze_symptoms(symptoms)
    return jsonify({"result": result})

@api_bp.route('/get_literature', methods=['POST'])
def get_literature():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = medical_literature_service.get_relevant_literature(query)
    return jsonify({"result": result})

@api_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    try:
        patient = patient_service.create_patient(data)
        return jsonify(patient), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = patient_service.get_patient(patient_id)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404

@api_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    patient = patient_service.update_patient(patient_id, data)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404

@api_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if patient_service.delete_patient(patient_id):
        return '', 204
    return jsonify({"error": "Patient not found"}), 404

@api_bp.route('/patients', methods=['GET'])
def list_patients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    patients = patient_service.list_patients(page, per_page)
    return jsonify(patients) """