import cv2
import mediapipe as mp
import numpy as np
import time

camera = cv2.VideoCapture(0)
res_x = 1280
res_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, res_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, res_y)

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

left_eye = [385, 380, 387, 373, 362, 263]
right_eye = [160, 144, 158, 153, 33, 133]
both_eyes = left_eye + right_eye
limit_ear = 0.35
dormindo = 0

mouth = [82, 87, 13, 14, 312, 317, 78, 308]
limit_mar = 0.3

temp_timer = 0
temp_counter = 0
counter_list = []

blink_counter = 0
blink_timer = time.time()

def ear_calc(face, left_eye, right_eye):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        left_face = face[left_eye,:]
        right_face = face[right_eye,:]

        left_ear = (np.linalg.norm(left_face[0]-left_face[1])+np.linalg.norm(left_face[2]-left_face[3]))/(2*(np.linalg.norm(left_face[4]-left_face[5])))
        right_ear = (np.linalg.norm(right_face[0]-right_face[1])+np.linalg.norm(right_face[2]-right_face[3]))/(2*(np.linalg.norm(right_face[4]-right_face[5])))
    except:
        left_ear = 0.0
        right_ear = 0.0
    median_ear = (left_ear + right_ear)/2
    return median_ear

def mar_calc(face, mouth):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_mouth = face[mouth,:]

        mar = (np.linalg.norm(face_mouth[0]-face_mouth[1])+np.linalg.norm(face_mouth[2]-face_mouth[3])+np.linalg.norm(face_mouth[4]-face_mouth[5]))/(2*(np.linalg.norm(face_mouth[6]-face_mouth[7])))
    except:
        mar = 0.0
    return mar

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_detection:
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            print('Ignoring empty camera frame.')
            continue
        length, width, _ = frame.shape
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 102, 102), thickness=1, circle_radius=1),
                                            connection_drawing_spec=mp_drawing.DrawingSpec(color=(102, 204, 0), thickness=1, circle_radius=1))
                face = face_landmarks
                for coord_id, coord_xyz in enumerate(face.landmark):
                    if (coord_id in both_eyes):
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, width, length)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                    if (coord_id in mouth):
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, width, length)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                ear = ear_calc(face.landmark, left_eye, right_eye)
                cv2.rectangle(frame, (0, 1), (290,140), (58, 58, 55), -1)
                cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 24), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                mar = mar_calc(face.landmark, mouth)
                cv2.putText(frame, f"MAR: {round(mar, 2)} {'Open' if mar>=limit_mar else 'Closed'}", (1, 50),
                                cv2.FONT_HERSHEY_DUPLEX,
                                0.9, (255, 255, 255), 2)

                if (ear < limit_ear and mar < limit_mar):
                    start_time = time.time() if dormindo == 0 else start_time
                    blink_counter = blink_counter + 1 if dormindo == 0 else blink_counter
                    dormindo = 1
                if (dormindo == 1 and ear >= limit_ear) or (ear <= limit_ear and mar >= limit_mar):
                    dormindo = 0
                final_time = time.time()
                elapsed_time = final_time - blink_timer

                if elapsed_time >= (temp_timer + 1):
                    temp_timer = elapsed_time
                    blink_per_seconds = blink_counter - temp_counter
                    temp_counter = blink_counter
                    counter_list.append(blink_per_seconds)
                    counter_list = counter_list if len(counter_list) <= 60 else counter_list[-60:]
                blinks_per_minute = 15 if elapsed_time <= 60 else sum(counter_list)
                
                cv2.putText(frame, f"BLINKS: {blink_counter}", (1, 120), cv2.FONT_HERSHEY_DUPLEX, 0.9, (109, 233, 219), 2)
                final_time = final_time - start_time if dormindo == 1 else 0.0
                cv2.putText(frame, f"TIME: {round(final_time, 3)}", (1, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                if blinks_per_minute < 10 or final_time >= 1.5:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, "Caution! You may be sleepy", (80, 435), cv2.FONT_HERSHEY_DUPLEX, 0.85, (58, 58, 55), 1)

        except:
            pass

        cv2.imshow('camera', frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break
camera.release()
cv2.destroyAllWindows()