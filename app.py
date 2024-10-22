import os
import whisper
import requests
from gtts import gTTS
import tempfile
import gradio as gr

# Load the Whisper model
model = whisper.load_model("base")

GROQ_API_KEY="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"
Client = GROQ_API_KEY=GROQ_API_KEY

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result['text']

def get_response_from_groq(user_input):
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
    tts = gTTS(text=text, lang='en')
    audio_file = tempfile.NamedTemporaryFile(delete=True, suffix=".mp3")
    tts.save(audio_file.name)
    return audio_file.name

def chatbot(audio):
    transcribed_text = transcribe_audio(audio)
    response_text = get_response_from_groq(transcribed_text)
    audio_response = text_to_audio(response_text)
    return audio_response

iface = gr.Interface(fn=chatbot, inputs=gr.Audio(source="microphone", type="filepath"), outputs="audio")
iface.launch()
