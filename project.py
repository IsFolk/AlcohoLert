import subprocess
import threading

def dataset():
    subprocess.Popen(["/home/pi/Desktop/project_use/build_dataset.sh"], stdin=subprocess.PIPE)
    
def embedding():
    subprocess.Popen(["/home/pi/Desktop/project_use/face_recog/extract_embeddings.sh"], stdin=subprocess.PIPE)

def recognizer():
    subprocess.Popen(["/home/pi/Desktop/project_use/face_recog/recognize_video.sh"], stdin=subprocess.PIPE)

data = threading.Thread(target=dataset)
embed = threading.Thread(target=embedding)
recog = threading.Thread(target=recog)