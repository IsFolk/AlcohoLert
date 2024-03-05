# import required modules
from pydub import AudioSegment
from pydub.playback import play
import threading
import multiprocessing
from multiprocessing import Process, Queue
import pygame

def blow_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/blow_notif.wav")
    #print('playing sound using  pydub')
    t = threading.Thread(target=play, args=(song,))
    t.start()


 
 
def confirmed_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/confirm_notif.wav")
    #print('playing sound using  pydub')
    play(song)
    
    
def recog_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/recog_notif.wav")
    #print('playing sound using  pydub')
    play(song)


def over_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/over.wav")
    #print('playing sound using  pydub')
    play(song)
    
    
def changePeople_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/changePeople.wav")
    #print('playing sound using  pydub')
    play(song)
    
    
def notBlow_notify():
    # for playing wav file
    song = AudioSegment.from_wav("/home/pi/Desktop/project_use/face_recog/mp3/notBlow.wav")
    #print('playing sound using  pydub')
    play(song)



def face_warning_notify():
    
    def play_pygame():
        pygame.mixer.init()
        pygame.mixer.music.load('/home/pi/Desktop/project_use/face_recog/mp3/face_warning.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    
    t = threading.Thread(target=play_pygame)
    t.start()

