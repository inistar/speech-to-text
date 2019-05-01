# Import Packages
import os
from google.cloud import storage
import pyaudio
import wave

# Environment Variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\\GCP\\hackstaticboss\\Service Account Key\\hackathon-springml-2019.json'

# GCS Bucket Properties
bucket_name = 'speech-to-text-hackathon'
source_file_name = 'E:\\file.wav'
destination_blob_name = 'sample.wav'

# Audio File Properties
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "E:\\file.wav"


def record():
    # PyAudio Object
    audio = pyaudio.PyAudio()

    # Start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("recording...")
    frames = []

    # To Stop Recording press CTRL + C
    try:
        while True:
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
    except KeyboardInterrupt:
        print('interrupted!')

    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # write to wave file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    # Uploads a file to the bucket.
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


# Function Call
record()
upload_to_bucket(bucket_name, source_file_name, destination_blob_name)
