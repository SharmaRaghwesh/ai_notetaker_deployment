import sounddevice as sd
import wavio
import os
from pydub import AudioSegment
import threading

def record_audio(stop_flag, output_wav, device_name="Meet Aggregate", fs=16000, chunk_minutes=3):
    chunk_seconds = chunk_minutes * 60
    chunk_files = []
    chunk_index = 1

    # Find input device
    device_index = None
    for i, d in enumerate(sd.query_devices()):
        if device_name.lower() in d["name"].lower():
            device_index = i
            break
    if device_index is None:
        raise ValueError(f"Device '{device_name}' not found. Available: {[d['name'] for d in sd.query_devices()]}")

    device_info = sd.query_devices(device_index)
    channels = device_info["max_input_channels"]

    try:
        while not stop_flag.is_set():
            print(f"🎙️ Recording chunk {chunk_index} …")
            recording = sd.rec(
                int(chunk_seconds * fs),
                samplerate=fs,
                channels=channels,
                dtype="int16",
                device=device_index
            )
            sd.wait()
            chunk_file = f"chunk_temp_{chunk_index}.wav"
            wavio.write(chunk_file, recording, fs, sampwidth=2)
            chunk_files.append(chunk_file)
            print(f"✅ Saved {chunk_file}")
            chunk_index += 1
    except Exception as e:
        print("⚠️ Recording stopped early:", e)

    # Merge chunks
    if chunk_files:
        audio = AudioSegment.empty()
        for f in chunk_files:
            audio += AudioSegment.from_wav(f)
        audio.export(output_wav, format="wav")
        print(f"🎉 Final meeting recording saved as {output_wav}")
        for f in chunk_files:
            os.remove(f)
