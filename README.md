# 🎙️ Voice Emotion Analyzer Agent

This project is an **AI-powered voice emotion analyzer and companion** that listens to your voice, transcribes it, detects emotions from both **audio tone** and **text meaning**, and responds with a supportive message using **GPT** and **ElevenLabs Text-to-Speech**.

## 🚀 Features
- 🎤 **Voice Recording** — Captures audio from your microphone
- 📝 **Speech-to-Text** — Uses OpenAI Whisper to transcribe speech
- 🎧 **Audio Emotion Detection** — Detects mood from pitch and energy
- 💬 **Text Emotion Analysis** — Uses a transformer model to classify emotion from words
- 🤖 **AI Responses** — Generates supportive replies with GPT
- 🔊 **Voice Output** — Speaks replies via ElevenLabs TTS
- 🎶 Optional background sounds for uplifting messages

---

## 📦 Requirements

### 1. Install Dependencies
Make sure you have Python 3.9+ installed, then run:

pip install -r requirements.txt


### 2. ⚙️ Setup

**1. Install FFmpeg**
Whisper and Librosa require FFmpeg.
Download FFmpeg and add its /bin folder to your system PATH.
Example (Windows):
makefile
Copy
Edit
C:\ffmpeg-7.0.2-essentials_build\bin

**2. Environment Variables**
Create a .env file in the project root:
ini
Copy
Edit
```
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

**3. Optional Audio Files**
Place an uplifting background track as calm.mp3 in the project directory.

### 3. ▶️ Usage
```
Run the program:
bash
Copy
Edit
python voice.py
```
```
Flow:
Records 6 seconds of your voice
Transcribes with Whisper
Detects both audio and text emotion
Chooses final emotion (text > audio)
Responds using GPT + ElevenLabs
```
## 🧠 Emotion Logic
Sad → Plays uplifting message + calm music
Happy → Responds cheerfully with AI-generated reply

## ⚠️ Notes
Large .dll or .lib files from virtual environments should be excluded from Git using .gitignore
GitHub file size limit is 100 MB — avoid committing virtual environments
Neutral → Provides general supportive response

<img width="1515" height="319" alt="Screenshot 2025-08-12 191219" src="https://github.com/user-attachments/assets/18ee99af-da18-4dd9-9e20-54b7580f2f5e" />


