from whisper_timestamped import transcribe
import whisper_timestamped as WhisperTimestamped
import json
# Install whisper-timestamped if you haven't already:
# pip install whisper-timestamped

# Replace "your_audio_file.wav" with the path to your audio file
audio_path = "audio.wav"

# Specify language (optional, defaults to 'en')
language = "en"

# Create WhisperTimestamped instance
model = WhisperTimestamped.load_model("base")

# Process audio and get word-level timestamps
result = model.transcribe(audio_path)

# result will be a list of dictionaries containing 'text' and 'timestamp' keys
res = result
try:
  for i in range(len(res)):

    print(f"{res[0]}: {res[0]}")
except IndexError:
  print("There might be fewer words than expected.")
  
  
  