#Importing Pytube library
import pytube
# Reading the above Taken movie Youtube link
video = "https://www.youtube.com/watch?v=6QY8sHifKsw&ab_channel=ShrishailNagral"
data = pytube.YouTube(video)
# Converting and downloading as 'MP4' file
audio = data.streams.get_audio_only()
audio.download()