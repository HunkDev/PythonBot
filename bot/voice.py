import whisper
import sounddevice as sd
from scipy.io.wavfile import write

model = whisper.load_model("base")

def record_audio(filename=r"c:\Users\serge\source\repos\Python\AI\bot\input.wav", seconds=4, fs=16000):
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)

def speech_to_text(filename=r"c:\Users\serge\source\repos\Python\AI\bot\input.wav"):
    result = model.transcribe(filename, language="ru")
    return result["text"]

def listen():
    record_audio()
    text = speech_to_text()
    return text