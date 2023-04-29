import whisper
whisper.DecodingOptions(fp16 = False)
print("whisper imported  ")
model = whisper.load_model("large")
print("model created")
# load audio and pad/trim it to fit 30 seconds
print("start loading the audio file")
audio = whisper.load_audio("../src/audio/recordedfiles/voicerecord2023-21-43-20.wav")
audio = whisper.pad_or_trim(audio)
print("loaded audio files and trimmed it")
# make log-Mel spectrogram and move to the same device as the model
text = model.transcribe(audio)
print("extracted the text fom audio")
print(text)
print(text.values())
print("done")
# mel = whisper.log_mel_spectrogram(audio).to(model.device)
#
# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")
#
# # decode the audio
# options = whisper.DecodingOptions(fp16 = False)
#
# result = whisper.decode(model, mel, options)
#
# # print the recognized text
# print(result.text)