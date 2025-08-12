import os
import openai
import requests
import librosa
import numpy as np
import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
from dotenv import load_dotenv
from transformers import pipeline
from playsound import playsound


# Force-add FFmpeg path for virtual environment
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.0.2-essentials_build\bin"

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
openai.api_key = OPENAI_API_KEY

# Whisper model
whisper_model = whisper.load_model("base")

# 1. Record from microphone (5 seconds default)
def record_audio(filename="mic_input.wav", duration=5, fs=16000):
    print("🎙️ Recording... Speak now.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)
    print("✅ Recording saved as", filename)

# 2. Transcribe using Whisper
def transcribe_whisper(audio_path: str) -> str:
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# 3. Audio emotion via pitch/energy
def extract_audio_emotion(audio_path: str) -> str:
    y, sr = librosa.load(audio_path)
    pitch = librosa.yin(y, fmin=50, fmax=300)
    energy = np.sum(np.square(y))
    avg_pitch = np.mean(pitch)
    if avg_pitch < 130 and energy < 0.01:
        return "sad"
    elif avg_pitch > 200 and energy > 0.03:
        return "happy"
    else:
        return "neutral"

# 4. Text emotion detection
def detect_text_emotion(text: str) -> str:
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    result = classifier(text)[0]
    return result["label"].lower()

# 5. GPT reply
def generate_gpt_reply(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a kind and supportive AI companion."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message["content"]

# 6. ElevenLabs TTS
def speak_with_elevenlabs(text: str, voice="Rachel"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open("response_audio.mp3", "wb") as f:
            f.write(response.content)
        playsound("response_audio.mp3")
    else:
        print("Error from ElevenLabs:", response.text)

# 7. Respond based on emotion
def respond_to_emotion(emotion: str, user_text: str):
    if emotion == "sad":
        print("🎵 Emotion: Sad. Playing uplifting message...")
        speak_with_elevenlabs("I'm here for you. Let's do something uplifting together.")
        playsound("calm.mp3")  # Add a file named calm.mp3
    elif emotion == "happy":
        print("😊 Emotion: Happy. Responding cheerfully...")
        reply = generate_gpt_reply(user_text)
        speak_with_elevenlabs(reply)
    else:
        print("😐 Emotion: Neutral or mixed. Offering general support...")
        reply = generate_gpt_reply(user_text)
        speak_with_elevenlabs(reply)

# 🎯 Main function
def main():
    record_audio("input.wav", duration=6)
    print("🔊 Transcribing...")
    text = transcribe_whisper("input.wav")
    print("📝 You said:", text)

    audio_emotion = extract_audio_emotion("input.wav")
    text_emotion = detect_text_emotion(text)

    print("🎧 Audio Emotion:", audio_emotion)
    print("💬 Text Emotion:", text_emotion)

    final_emotion = text_emotion if text_emotion != "neutral" else audio_emotion
    respond_to_emotion(final_emotion, text)

# 🚀 Run
if __name__ == "__main__":
    main()
