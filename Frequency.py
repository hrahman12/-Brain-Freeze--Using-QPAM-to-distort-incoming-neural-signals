import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

def plot_frequency_content(filename):
    # Read the WAV file
    sample_rate, data = scipy.io.wavfile.read(filename)
    print(sample_rate)
    if len(data.shape) == 2:
        data = data.mean(axis=1) # Take the mean across axis 1 (channel) to get mono audio
    
    # Use Fourier Transform to understand frequency
    # Use np.fft.rfft to do DFT (Discrete Fourier Transform)
    freq_data = np.fft.rfft(data)

    # Compute the power spectrum by obtaining the magnitudes of the Fourier coefficients.
    power_spectrum = np.abs(freq_data)
    
    # Calculate frequencies corresponding to the positive half of the Fourier transform output
# Using np.fft.rfftfreq to generate frequency array based on data length and sample rate
    freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)
    
    # code for plot
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, power_spectrum)
    plt.title(f'Frequency Content of {filename}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.yscale('log')  
    plt.xlim(0, sample_rate / 2)  # Set the x-axis limits to show frequencies ranging from 0 up to half of the sampling rate
    plt.grid(True)
    plt.show()

print("Files starting with 'PoissonWake':")
filenames = [filename for filename in matching_files]
# Replace with your file names
for filename in filenames:
    plot_frequency_content(filename)
