import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

st.title("Voice-to-Text with Recording")

# Include the recording JavaScript
st.markdown("""
<script src="record.js"></script>
<button id="record-button">Start Recording</button>
<button id="stop-button" disabled>Stop Recording</button>
<audio id="audio-preview" controls></audio>
<input type="hidden" id="audio-data" />
""", unsafe_allow_html=True)

# Upload the recorded file
audio_url = st.text_input("Audio URL", "")
if audio_url:
    # Convert the Blob URL to binary data
    audio_blob = BytesIO(requests.get(audio_url).content)
    
    recognizer = sr.Recognizer()

    try:
        # Recognize the audio file
        audio = AudioSegment.from_wav(audio_blob)
        with sr.AudioFile(audio_blob) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            st.write("Transcription:")
            st.write(text)
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
