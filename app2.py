import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Title of the app
st.title("Voice-to-Text with Dynamic Recording")

# Frontend HTML & JavaScript for audio recording
st.markdown("""
    <h3>Record your audio</h3>
    <button id="recordButton">Start Recording</button>
    <button id="stopButton" disabled>Stop Recording</button>
    <p><strong>Recording:</strong> <span id="recordingStatus">Not started</span></p>
    <audio id="audioPlayback" controls></audio>
    <br>

    <script>
        let chunks = [];
        let recorder;
        let audioBlob;

        document.getElementById('recordButton').onclick = async function() {
            chunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                audioBlob = new Blob(chunks, { 'type': 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('audioPlayback').src = audioUrl;
                document.getElementById('audioData').value = audioUrl;
            };
            recorder.start();
            document.getElementById('recordingStatus').innerText = 'Recording...';
            document.getElementById('recordButton').disabled = true;
            document.getElementById('stopButton').disabled = false;
        }

        document.getElementById('stopButton').onclick = function() {
            recorder.stop();
            document.getElementById('recordingStatus').innerText = 'Recording stopped';
            document.getElementById('recordButton').disabled = false;
            document.getElementById('stopButton').disabled = true;
        }
    </script>
""", unsafe_allow_html=True)

# Hidden field to get the audio data
audio_url = st.text_input("Paste audio URL (after recording):")

# Transcription part if an audio is available
if audio_url:
    st.write("Transcribing your audio...")
    
    # Process the audio file from the URL
    recognizer = sr.Recognizer()

    try:
        # Load audio from Blob URL and transcribe
        audio = BytesIO(requests.get(audio_url).content)
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            st.write("Transcription:")
            st.write(transcription)
    except sr.UnknownValueError:
        st.write("Sorry, we couldn't understand the audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
