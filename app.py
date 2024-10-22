import os
import whisper
import requests
from gtts import gTTS
import tempfile
import streamlit as st

# Load the Whisper model
model = whisper.load_model("base")  # Choose your model size

# Set your API key here
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual API key

def transcribe_audio(audio_file):
    """Transcribe audio to text using Whisper."""
    result = model.transcribe(audio_file)
    return result['text']

def get_response_from_groq(user_input):
    """Get response from Groq API using requests."""
    api_key = os.environ.get("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "model": "llama3-8b-8192"
    }
    response = requests.post("https://api.groq.ai/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

def text_to_audio(text):
    """Convert text to audio using gTTS."""
    tts = gTTS(text=text, lang='en')
    audio_file = tempfile.NamedTemporaryFile(delete=True, suffix=".mp3")
    tts.save(audio_file.name)
    return audio_file.name

def main():
    st.title("Voice Chatbot")
    
    # File uploader for audio input
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file is not None:
        # Transcribe audio to text
        transcribed_text = transcribe_audio(audio_file)
        st.write("Transcribed Text:", transcribed_text)
        
        # Get response from Groq API
        response_text = get_response_from_groq(transcribed_text)
        st.write("Response Text:", response_text)

        # Convert response text to audio and play it
        audio_response = text_to_audio(response_text)
        st.audio(audio_response, format='audio/mp3')

if __name__ == "__main__":
    main()
