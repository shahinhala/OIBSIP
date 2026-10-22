# Voice Assistant — Python GUI

A beginner-friendly desktop voice assistant created for a Python programming internship project. It supports typed commands by default, optional microphone input, text-to-speech responses, and opening common websites/searches.

## Features
- Tkinter graphical interface
- Typed command support even without microphone packages
- Optional voice input with SpeechRecognition and PyAudio
- Spoken responses using pyttsx3 when installed
- Tells the current time and date
- Opens Google, YouTube, Gmail, Wikipedia, and GitHub
- Searches the web using a browser
- Handles unrecognized commands and common voice-input errors

## Files
- `voice_assistant.py` — main application
- `requirements.txt` — optional dependencies
- `README.md` — project instructions

## Requirements
- Python 3
- Tkinter (normally included with Windows Python)
- Optional packages for voice features: `pyttsx3`, `SpeechRecognition`, and `PyAudio`

## Setup
Open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

If PyAudio installation fails, the assistant can still run with typed commands. You can install `pyttsx3` separately for spoken responses:

```bash
python -m pip install pyttsx3
```

## Run
```bash
python voice_assistant.py
```

On Windows, you can also try:
```bash
py voice_assistant.py
```

## Example commands
- `time`
- `date`
- `open Google`
- `open YouTube`
- `open Gmail`
- `open GitHub`
- `search Python programming`
- `help`
- `exit`

## Notes
- Microphone input requires a working microphone and the optional SpeechRecognition/PyAudio packages.
- Google speech recognition is used for microphone transcription and therefore requires internet access.
- This is a learning/demo project, not a full AI assistant.
- Do not speak passwords or other sensitive information into speech-recognition services.

## Internship submission checklist
- Run the application and test typed commands.
- If voice dependencies are installed, test the microphone button too.
- Capture screenshots of the GUI and sample command outputs.
- Upload the source code, README, and screenshots according to the exact folder structure in your internship instructions.
