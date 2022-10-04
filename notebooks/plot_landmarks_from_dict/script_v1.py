import pandas as pd
import numpy as np
import cv2 as cv
import mediapipe as mp
import sys
print(sys.version)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def plot_ldmks(image, ldmks):
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
    ) as face_mesh:
        height, width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
            return None
        face_landmarks = results.multi_face_landmarks[0]  # Using first face detected only

        for ldmk in ldmks:
            if pd.isnull(ldmk):
                continue
            ldmk = int(ldmk)

            pt1 = face_landmarks.landmark[ldmk]
            x = int(pt1.x * width)
            y = int(pt1.y * height)
            cv.circle(image, (x, y), 5, (100, 100, 0), -1)
            cv.putText(image, str(ldmk), (x, y), 1, 1, (0, 0, 0))
        cv.imwrite(
            'D:\\Google Drive\\Facul\\ENG\\5 ano\\TCC\\apps_hibridos\\api_facs\\'
            'notebooks\\plot_landmarks_from_dict\\results\\image.png',
            image
        )
        return image


df_ldmk = pd.read_csv(
    'D:\\Google Drive\\Facul\\ENG\\5 ano\\TCC\\apps_hibridos\\api_facs\\src\\api\\data\\dict_landmarks.csv',
    index_col=0)
df_ldmk['landmarks'] = df_ldmk['landmarks'].apply(
    lambda ldmk: np.unique(
        np.array(
            ldmk.split(',')
        ).astype(np.float16)
    ) if pd.notnull(ldmk) else np.nan
)

aus = [
    4,
    5,
    7,
    23
]
ldmks = np.array([])
for au in aus:
    ldmks = np.append(ldmks, df_ldmk.loc[au, 'landmarks'])
ldmks = np.unique(ldmks)

img = cv.imread(
    'D:\\Google Drive\\Facul\\ENG\\5 ano\\TCC\\apps_hibridos\\api_facs\\notebooks'
    '\\plot_landmarks_from_dict\\data\\test_img.jpg'
)

img_res = plot_ldmks(img, ldmks)

cv.namedWindow('output', cv.WINDOW_NORMAL)
cv.imshow('output', img_res)  # [450:1400, 150:1000])  # Show image
cv.waitKey(0)  # Display the image infinitely until any keypress
