# import required modules
from pydub import AudioSegment
from pydub.playback import play
  
# for playing wav file
song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/blow_notif.wav")
print('playing sound using  pydub')
play(song)