import pennylane as qml
import pennylane.numpy as np
import scipy.io.wavfile
import wave
import time


def load_wav(filename):
    sample_rate, data = scipy.io.wavfile.read(filename)
    # If the audio file is stereo, average the channels to convert to mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    return sample_rate, data

#save audio data as WAV file
def save_wav(filename, sample_rate, data):
    scipy.io.wavfile.write(filename, sample_rate, data)

# 8 bit format conversion
def convert_to_8bit(data):
    # Here we normalize data in range [-128, 127]
    data = ((data - data.min()) / (data.max() - data.min()) * 255 - 128).astype(np.int8)
    return data

# qubits used in the quantum circuit
NB_QUBITS = 21

# Audio parameters
sample_rate = 44100  # Sampling rate in Hz
duration = 0.2  # Duration of audio in seconds
frequency = 440  # Frequency of the sine wave in Hz
amplitude = 2**(NB_QUBITS-1)/2-1  # Maximum amplitude for an N-bit audio file

# PennyLane quantum device
dev = qml.device("default.qubit", wires=range(NB_QUBITS), shots=1)

# Generate a sine wave for classical processing
#t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
#samples = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

# Load data 
filename = 'PoissonWake'
sample_rate, original_data = load_wav(filename)

# Convert original audio data to 8-bit 
#data_8bit = original_data  
convert_to_8bit(original)data)

save_wav(f'original_8bit_{filename}.wav', sample_rate, data_8bit)

# Store the 8-bit version of the original audio data in the 'samples' variable
samples = data_8bit

# Quantum processing
quantum_samples = []

#  mapping function
low1 = -amplitude
low2 = 0
high1 = amplitude
high2 = 2*np.pi

def remapTo2Pi(value):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

#create a new qc circuit
@qml.qnode(dev)
def circuit1(global_iterator):
    for i in range(NB_QUBITS):
        if global_iterator < len(samples):
            qml.RX(remapTo2Pi(samples[global_iterator]), i)
    return [qml.sample(qml.PauliZ(i)) for i in range(NB_QUBITS)]

# loop to repeat the circuit for number of samples
for i in range(len(samples)):
    sample = circuit1(i)

    # Convert quantum measurement results to a binary representation
    normal_list = [array.item() for array in sample]
    adjusted_list = [0 if x == -1 else 1 for x in normal_list]  # Map -1 to 0 and 1 to 1
    binary_string = ''.join(map(str, adjusted_list))  # Convert list to binary string
    binary_to_int = int(binary_string, 2)  # Convert binary string to integer

    quantum_samples.append(binary_to_int)
    if i % 1000 == 0:
        print(i)

# Create a new WAV file containing the quantum-processed audio data
with wave.open(f'mega{time.time()}.wav', 'w') as wav_file:
    # Set parameters for the new WAV file
    wav_file.setparams((1, 2, sample_rate, len(samples), 'NONE', 'not compressed'))

    # Write to a new WAV file
    quantum_samples_array = np.array(quantum_samples, dtype=np.int16)
    wav_file.writeframes(np.array(quantum_samples_array).tobytes())

print("WAV file has been created.")
