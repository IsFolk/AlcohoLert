#!/bin/sh

#人臉偵測資料集
python3 face_detect.py --cascade /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml       --output /home/pi/Desktop/project_use/face_recog/dataset/test

#圖片處理
python extract_embeddings.py \
	--dataset dataset \
	--embeddings output/embeddings.pickle \
	--detector face_detection_model \
	--embedding-model face_embedding_model/openface_nn4.small2.v1.t7
#資料處理trainmodel
python train_model.py --embeddings output/embeddings.pickle \
	--recognizer output/recognizer.pickle --le output/le.pickle
#辨識
python recognize_video.py --detector face_detection_model \
	--embedding-model face_embedding_model/openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle
