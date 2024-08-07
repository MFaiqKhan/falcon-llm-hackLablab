# MediMentor

MediMentor is an advanced medical assistant application that utilizes Retrieval-Augmented Generation (RAG) with the Falcon Large Language Model (LLM) to provide accurate and context-aware medical information.

## Features

1. **Audio Interaction Endpoint**
   - Speech-to-Text (S2T) conversion
   - LLM processing using Falcon
   - Text-to-Speech (T2S) conversion for audible responses

2. **Text-based Interaction Endpoint**
   - Direct text input
   - LLM processing using Falcon
   - Text output

3. **Retrieval-Augmented Generation (RAG)**
   - Enhances responses with relevant medical knowledge
   - Improves accuracy and context-awareness of the AI

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/medimentor.git
   cd medimentor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   AI71_API_KEY=your_ai71_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

4. Initialize the Qdrant database (if not already done):
   ```
   python data_ingestion.py
   ```

## Usage

Run the Flask application:
```
python run.py
```

The server will start, typically on `http://127.0.0.1:3030`.

### 1. Audio Endpoint

- **URL**: `/api/chat/audio`
- **Method**: POST
- **Description**: This endpoint accepts audio input, transcribes it, processes it through the Falcon LLM, and returns an audio response.

**Example using cURL**:
```bash
curl -X POST http://127.0.0.1:3030/api/chat/audio -H "Content-Type: audio/wav" --data-binary @your_audio_file.wav -o response.wav
```

### 2. Text Endpoint

- **URL**: `/api/chat/text`
- **Method**: POST
- **Description**: This endpoint accepts text input, processes it through the Falcon LLM, and returns a text response.

**Example using cURL**:
```bash
curl -X POST http://127.0.0.1:3030/api/chat/text \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the symptoms of schizophrenia?"}'
```

## Architecture

MediMentor uses a Retrieval-Augmented Generation (RAG) architecture:

1. User input (text or transcribed audio) is processed.
2. Relevant medical information is retrieved from the Qdrant vector database.
3. The Falcon LLM generates a response based on the user query and retrieved information.
4. The response is returned as text or converted to speech.

## Contributing

Contributions to MediMentor are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- AI71 for providing the Falcon LLM API
- Qdrant for vector database capabilities
- All contributors and supporters of the MediMentor project