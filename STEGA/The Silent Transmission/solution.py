import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# --- Read the WAV file ---
with wave.open("original.wav", "rb") as wav_file:
    sample_rate = wav_file.getframerate()  # Get sample rate (e.g., 44100 Hz)
    n_frames = wav_file.getnframes()      # Total number of frames
    audio = wav_file.readframes(n_frames) # Read raw audio data

# Convert raw bytes to numpy array (16-bit PCM assumed)
audio = np.frombuffer(audio, dtype=np.int16)

# --- Generate Spectrogram ---
frequencies, times, spectrogram = signal.spectrogram(audio, sample_rate)
plt.pcolormesh(times, frequencies, np.log(spectrogram))
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [sec]")
plt.title("Spectrogram of 'original.wav' - Look for high-frequency spikes!")
plt.colorbar(label="Intensity (dB)")
plt.show()