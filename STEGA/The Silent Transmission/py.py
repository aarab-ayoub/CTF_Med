import numpy as np
import wave
import struct

# --- SETUP ---
flag = "CTF{SP3CTR0GR4M5_R0CK}"  # The hidden flag
sample_rate = 44100  # Standard audio sample rate (Hz)
duration = 5.0  # Audio duration (seconds)
freq_noise = 500  # Base noise frequency (Hz)
freq_flag = 15000  # High frequency where the flag is hidden (Hz)

# --- GENERATE AUDIO ---
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 1. Create background noise (masking sound)
noise = np.sin(2 * np.pi * freq_noise * t) * 0.3  # Lower-frequency sine wave

# 2. Encode the flag in high-frequency Morse/beeps
flag_signal = np.zeros_like(t)
for i, char in enumerate(flag):
    # Turn each character into a binary sequence (simplified)
    binary_char = bin(ord(char))[2:].zfill(8)
    for j, bit in enumerate(binary_char):
        if bit == '1':
            start = i * 0.2 + j * 0.02  # Timing for each bit
            end = start + 0.01
            mask = (t >= start) & (t <= end)
            flag_signal[mask] += np.sin(2 * np.pi * freq_flag * t[mask]) * 0.5

# Combine signals
audio = noise + flag_signal
audio = (audio * 32767).astype(np.int16)  # Convert to 16-bit PCM

# --- SAVE AS WAV ---
wav_file = wave.open("original.wav", "wb")
wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 2 bytes (16-bit)
wav_file.setframerate(sample_rate)
wav_file.writeframes(audio.tobytes())
wav_file.close()

print("Generated original.wav! Open it in a spectrogram viewer (e.g., Audacity).")