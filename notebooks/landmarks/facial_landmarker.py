import cv2
import numpy as np
import dlib

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
FACE_RECT_COLOR = BLUE
LANDMARKS_COLOR = RED

WEBCAM_NUMBER = 0
WEBCAM_FPS = 30
WEBCAM_PERIOD = int(1 / WEBCAM_FPS * 1000)

cap = cv2.VideoCapture(WEBCAM_NUMBER)
if cap is None or not cap.isOpened():
       raise Exception('Unable to open VideoCapture source.')
# cap.open(0, cv2.CAP_DSHOW)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./notebooks/landmarks/data/shape_predictor_68_face_landmarks.dat')  # Mudar para nome do arquivo que tem os pontos que queremos marcar na face

# Loop que matem ativo processamento de imagem para do video, ja que o OPENCV trabalha frame a frame (como se fosse varias imagens)
while(cap.isOpened()):
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    #logica para identificar o rosto  e marcar os pontos de interesse passado no modelo do arquivo
    for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            # cv2.rectangle(frame, (x1, y1), (x2, y2), FACE_RECT_COLOR, 3)
            landmarks = predictor(gray, face)

        #loop que de fato marca os pontos no rosto identificado
            for n in range(len(landmarks.parts())):
                x = landmarks.part(n).x
                y = landmarks.part(n).y

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    LANDMARKS_COLOR,
                    -1
                )
                cv2.putText(
                    frame,
                    str(n),
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    .5,
                    LANDMARKS_COLOR,
                    1,
                    2
                )

    cv2.waitKey(WEBCAM_PERIOD)
    cv2.imshow('frame', frame)
    # cv2.imwrite('./notebooks/landmarks/results/landmarks_output_example.jpg', frame)
