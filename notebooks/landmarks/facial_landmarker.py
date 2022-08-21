import cv2
import numpy as np
import dlib
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./notebooks/landmarks/shape_predictor_68_face_landmarks.dat')  # Mudar para nome do arquivo que tem os pontos que queremos marcar na face

# Loop que matem ativo processamento de imagem para do video, ja que o OPENCV trabalha frame a frame (como se fosse varias imagens)
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)

#logica para identificar o rosto  e marcar os pontos de interesse passado no modelo do arquivo
for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        landmarks = predictor(gray, face)
	
	#loop que de fato marca os pontos no rosto identificado
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
