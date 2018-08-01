import numpy as np
import time
import cv2
import glob
from pynput.keyboard import Key, Controller
from mss import mss

def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

sct = mss()
# The screen part to capture

# 1440p monitor parameteres
top = 300
left = 943
width = 675
height = 200

monitor = {'top': top, 'left': left, 'width': width, 'height': height}


left = 945
right = 1620
up = 300
down = 470

bbox = (left, up, right, down)

# trigger for window switching
time.sleep(2)

colors = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # idk
    (255, 0, 255),  # idk 2
    (0, 255, 255),  # idk 3
    (255, 192, 203),
    (115, 230, 42),
    (69, 69, 69),
    (209, 175, 21),
    (21, 175, 209),
]

game_over = cv2.imread('templates/game-over.png', 0)

templates_files = glob.glob('templates\\*.png')
print(templates_files)
templates = []

for image in templates_files:
    image = cv2.imread(image, 0)
    templates.append(image)

keyboard = Controller()

iter = 0
flag = False
while True:
    # print(iter)
    iter += 1
    if iter % 10 == 0 or flag:
        iter = 1
        keyboard.release(Key.down)
        keyboard.press(Key.up)
        keyboard.release(Key.up)
        flag = False
    else:
        keyboard.press(Key.down)
    sct_img = np.array(sct.grab(monitor))
    sct_grey = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)

    for idx, template in enumerate(templates):
        # if idx > 0:
        #     continue
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(sct_grey, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95

        loc = np.where( res >= threshold )
        coordinates = zip(*loc[::-1])
        # print(*coordinates)

        if loc[0].any():
            pt = next(coordinates)
            cv2.rectangle(sct_img, pt, (pt[0] + w, pt[1] + h), colors[idx], 2)
            if is_similar(template, game_over):
                print(pt, (pt[0] + w, pt[1] + h))
                flag = True

    cv2.imshow('window', sct_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
