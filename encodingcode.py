import pennylane as qml
import pennylane.numpy as np
import scipy.io.wavfile
import wave
import time
import math
import matplotlib.pyplot as plt


def load_wav(filename):
    sample_rate, data = scipy.io.wavfile.read(filename)
    
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    return sample_rate, data


def save_wav(filename, sample_rate, data):
    scipy.io.wavfile.write(filename, sample_rate, data)


def convert_to_8bit(data):
    
    data = ((data - data.min()) / (data.max() - data.min()) * 255 - 128).astype(np.int8)
    return data

filename = 'PoissonWake.wav'  # input file
sample_rate, original_data = load_wav(filename)

print("done converting wav data")

def QPAM_Encoding_Normalization(samples):
    
    normalized_arr = 2 * (samples - np.min(samples)) / (np.max(samples) - np.min(samples))

    

    np_data = np.array(normalized_arr)
    np_data += 1
    np_data /= 2
    sum = np.sum(np_data)
    np_data = np_data/sum

    print(np_data)
    return np_data

features = QPAM_Encoding_Normalization(original_data)
length = features.shape[0]
nb_qubits = math.ceil(np.log2(length))
print(f"number of qubits used for encoding: {nb_qubits}")
dev = qml.device('default.qubit', wires=nb_qubits)

@qml.qnode(dev)
def circuit(f=None):
    qml.AmplitudeEmbedding(features=f, wires=range(nb_qubits), pad_with=0,normalize=True)
    return qml.probs(wires=range(nb_qubits))
results = circuit(features)
print(f"encoding result: {results}")
normalized_results = ((results - np.min(results)) / (np.max(results) - np.min(results))) * (32767 + 32768) - 32768


with wave.open(f'mega{time.time()}.wav', 'w') as wav_file:
    
    wav_file.setparams((1, 2, sample_rate, length, 'NONE', 'not compressed'))
    
    
    quantum_samples_array = np.array(normalized_results, dtype=np.int16)
    print(quantum_samples_array)
    wav_file.writeframes(np.array(quantum_samples_array).tobytes())

print(f"mega{time.time()}.wav file has been created.")

plt.figure(figsize=(10, 6))
plt.plot(normalized_results, marker='o')
plt.title("Array Data")
plt.xlabel("Index")
plt.ylabel("Value")
plt.grid(True)
plt.show()