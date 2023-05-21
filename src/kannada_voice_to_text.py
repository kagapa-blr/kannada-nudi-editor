import whisper
whisper.DecodingOptions(fp16 = False)
def convert_voice_to_text():
    print("whisper imported  ")
    model = whisper.load_model("large")
    print("model created")
    # load audio and pad/trim it to fit 30 seconds
    print("start loading the audio file")
    audio = whisper.load_audio("../src/utility/ರಾಷ್ಟ ಕವಿ ಕುವೆಂಪು ಅವರ  ಮೈಸೂರು ಆಕಾಶವಾಣಿ ವಿಶೇಷ ಸಂದರ್ಶನ.mp4")
    audio = whisper.pad_or_trim(audio)
    print("loaded audio files and trimmed it")
    # make log-Mel spectrogram and move to the same device as the model
    text = model.transcribe(audio)
    print("extracted the text fom audio")
    print(text)
    print(text.values())
    print("done")
    return
convert_voice_to_text()