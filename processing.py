import numpy as np
import soundfile as sf


def reduce_noise(input_path, output_path):
    """
    Reads a WAV file, applies a simple FFT-based
    low-pass filter, and saves the processed file.
    """

    # Read audio
    signal, fs = sf.read(input_path)

    # Convert stereo to mono if needed
    if len(signal.shape) > 1:
        signal = signal[:, 0]

    # FFT
    fft_signal = np.fft.fft(signal)

    # Frequency axis
    N = len(signal)
    frequencies = np.fft.fftfreq(N, d=1/fs)

    # Low-pass filter cutoff (4 kHz)
    cutoff = 4000

    # Keep only frequencies within ±4 kHz
    fft_filtered = fft_signal.copy()
    fft_filtered[np.abs(frequencies) > cutoff] = 0

    # Inverse FFT
    filtered_signal = np.real(np.fft.ifft(fft_filtered))

    # Normalize to avoid clipping
    max_val = np.max(np.abs(filtered_signal))
    if max_val > 0:
        filtered_signal = filtered_signal / max_val

    # Save processed audio
    sf.write(output_path, filtered_signal, fs)