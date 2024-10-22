import os
import whisper
import requests
from gtts import gTTS
import tempfile
import streamlit as st
import streamlit.components.v1 as components

# Load the Whisper model
model = whisper.load_model("base")

# Set your API key
os.environ["GROQ_API_KEY"] = "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"

def transcribe_audio(audio_file):
    result = model.transcribe(audio_file)
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

# JavaScript for capturing audio
audio_capture_code = """
<script>
async function startRecording() {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    let mediaRecorder = new MediaRecorder(stream);
    let audioChunks = [];

    mediaRecorder.ondataavailable = function(event) {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = function() {
        let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        let audioUrl = URL.createObjectURL(audioBlob);
        let audioElement = document.createElement('audio');
        audioElement.src = audioUrl;
        audioElement.controls = true;
        document.body.appendChild(audioElement);

        let reader = new FileReader();
        reader.onloadend = function() {
            let base64data = reader.result.split(',')[1];
            const payload = { 'audio': base64data };
            fetch('/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
        };
        reader.readAsDataURL(audioBlob);
    };

    mediaRecorder.start();
    setTimeout(() => {
        mediaRecorder.stop();
    }, 3000); // Stop recording after 3 seconds
}

startRecording();
</script>
"""

def main():
    st.title("Voice Chatbot")
    st.markdown(audio_capture_code, unsafe_allow_html=True)

    if st.button("Start Recording"):
        st.write("Recording... Please wait.")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file is not None:
        transcribed_text = transcribe_audio(audio_file)
        st.write("Transcribed Text:", transcribed_text)

        response_text = get_response_from_groq(transcribed_text)
        st.write("Response Text:", response_text)

        audio_response = text_to_audio(response_text)
        st.audio(audio_response, format='audio/mp3')

if __name__ == "__main__":
    main()
