import cv2
import mediapipe as mp
import os
from time import sleep
import numpy as np
from pynput.keyboard import Controller
from pynput.keyboard import Key

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()
colors = {
    'RED': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'BLUE': (255, 0, 0),
    'YELLOW': (0, 255, 255),
    'PURPLE': (255, 0, 255),
    'CYAN': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0)
}
camera = cv2.VideoCapture(0)
res_x = 1280
res_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, res_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, res_y)

notepad = False
keyboard_keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A','S','D','F','G','H','J','K','L'],
            ['Z','X','C','V','B','N','M', ',','.',' ']]
offset = 50
key_counter = 0
text = '>'
keyboard = Controller()
canvas_img = np.ones((res_y, res_x, 3), np.uint8)*255
pen_color = colors['BLACK']
pen_diameter = 5
canvas_x, canvas_y = 0, 0

def print_keyboard(img, pos, keyboard_key, size = 50, rectangle_color = colors['WHITE']):
    cv2.rectangle(img, pos, (pos[0]+size, pos[1]+size), rectangle_color, cv2.FILLED)
    cv2.rectangle(img, pos, (pos[0]+size, pos[1]+size), colors['CYAN'], 1)
    cv2.putText(img, keyboard_key, (pos[0]+15,pos[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, colors['BLACK'], 2)
    return img

def find_hand_coords(img, reverse_hands=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    all_hands = []
    if result.multi_hand_landmarks:
        for hand_side, hand_landmarks in zip(result.multi_handedness, result.multi_hand_landmarks):
            hand_info = {}
            coords = []
            for landmark in hand_landmarks.landmark:
                coord_x, coord_y, coord_z = int(landmark.x * res_x), int(landmark.y * res_y), int(landmark.z * res_x)
                coords.append((coord_x, coord_y, coord_z))

            hand_info['coords'] = coords
            if (reverse_hands):
                hand_info['side'] = 'Left' if hand_side.classification[0].label == 'Right' else 'Right'
            else:
                hand_info['side'] = hand_side.classification[0].label

            all_hands.append(hand_info)
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
    return img, all_hands

def rise_fingers(hand):
    fingers = []
    for finger_tip in [8, 12, 16, 20]:
        if (hand['coords'][finger_tip][1] < hand['coords'][finger_tip - 2][1]):
            fingers.append(True)
        else:
            fingers.append(False)
    return fingers

while True:
    success, img = camera.read()
    img = cv2.flip(img, 1)

    img, all_hands = find_hand_coords(img)

    if len(all_hands) == 1:
        if all_hands[0]['side'] == 'Left':
            pointer_x, pointer_y, pointer_z = all_hands[0]['coords'][8]
            cv2.putText(img, f'distance: {pointer_z}', (850, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colors['WHITE'], 2)
            fingers_info_hand_one = rise_fingers(all_hands[0])
            for line_index, keyboard_index in enumerate(keyboard_keys):
                for index, keyboard_key in enumerate(keyboard_index):
                    if sum(fingers_info_hand_one) <= 1:
                        keyboard_key = keyboard_key.lower()
                    img = print_keyboard(img, (offset+index*80, offset+line_index*80), keyboard_key)
                    if (offset+index*80 < pointer_x < offset*2+index*80) and (offset+line_index*80<pointer_y<offset*2+line_index*80):
                        img = print_keyboard(img, (offset+index*80, offset+line_index*80), keyboard_key, rectangle_color=colors['GREEN'])
                        if pointer_z < -120:
                            key_counter = 1
                            key_to_write = keyboard_key
                            img = print_keyboard(img, (offset+index*80, offset+line_index*80), keyboard_key, rectangle_color=colors['CYAN'])
                            
            if key_counter:
                key_counter += 1
                if key_counter == 3:
                    text += key_to_write
                    key_counter = 0
                    keyboard.press(key_to_write)

            if fingers_info_hand_one == [False, False, False, True] and len(text) > 1:
                text = text[:-1]
                keyboard.press(Key.backspace)
                sleep(0.15)

            cv2.rectangle(img, (offset, 450), (830, 500), colors['WHITE'], cv2.FILLED)
            cv2.rectangle(img, (offset, 450), (830, 500), colors['CYAN'], 1)
            cv2.putText(img, text[-40:], (offset, 480), cv2.FONT_HERSHEY_COMPLEX, 1, colors['BLACK'], 2)
            cv2.circle(img, (pointer_x, pointer_y), 7, colors['CYAN'], cv2.FILLED)

    if len(all_hands) == 1:
        if all_hands[0]['side'] == 'Right':
            fingers_info_hand_one = rise_fingers(all_hands[0])
            if fingers_info_hand_one == [True, False, False, False] and notepad == False:
                notepad = True
                os.startfile(r'C:Windows\system32\notepad.exe')
            if fingers_info_hand_one == [False, False, False, False] and notepad == True:
                notepad = False
                os.system('taskkill /im notepad.exe /f')
            if fingers_info_hand_one == [True, False, False, True]:
                break

    if len(all_hands) == 2:
        fingers_info_hand_one = rise_fingers(all_hands[0])
        fingers_info_hand_two = rise_fingers(all_hands[1])

        pointer_x_one, pointer_y_one, pointer_z_one = all_hands[0]['coords'][8]

        if sum(fingers_info_hand_two) == 1:
            pen_color = colors['GREEN']
        if sum(fingers_info_hand_two) == 2:
            pen_color = colors['BLUE']
        if sum(fingers_info_hand_two) == 3:
            pen_color = colors['RED']
        if sum(fingers_info_hand_two) == 4:
            pen_color = colors['BLACK']
        else:
            canvas_img = np.ones((res_y, res_x, 3), np.uint8)*255

        pen_diameter = int(abs(pointer_z_one))//3+5
        cv2.circle(img, (pointer_x_one, pointer_y_one), pen_diameter, pen_color, cv2.FILLED)
        if fingers_info_hand_one == [True, False, False, False]:
            if (canvas_x == 0 and canvas_y == 0):
                canvas_x, canvas_y = pointer_x_one, pointer_y_one
            cv2.line(canvas_img, (canvas_x, canvas_y), (pointer_x_one, pointer_y_one), pen_color, pen_diameter)
            canvas_x, canvas_y = pointer_x_one, pointer_y_one
        else:
            canvas_x, canvas_y = 0, 0
        
        img = cv2.addWeighted(img, 1, canvas_img, 0.2, 0)

    cv2.imshow("Image", img)
    cv2.imshow("Canvas", canvas_img)
    pressedKey = cv2.waitKey(1)
    if pressedKey == 27:
        break

with open('text.txt', 'w') as file:
    file.write(text)

cv2.imwrite('canvas.png', canvas_img)