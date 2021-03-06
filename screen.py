import cv2
import numpy as np
import glob
from random import sample
from mss import mss
from win32api import GetSystemMetrics
from functools import cmp_to_key


def get_monitor(top, left, width, height):
    return {'top': top, 'left': left, 'width': width, 'height': height}

grab_areas = {
    (2560, 1440): get_monitor(300, 943, 675, 200),
    (2048, 1152): get_monitor(300, 943, 675, 200),
	(1536, 864): get_monitor(345, 575, 750, 200),
}

screen_w = GetSystemMetrics(0)
screen_h = GetSystemMetrics(1)

monitor = grab_areas.get((screen_w, screen_h))
print(screen_h, screen_w, monitor)

sct = mss()


def grab_screen(color='rgb'):
    sct_img = np.array(sct.grab(monitor))
    if color == 'grey':
        return cv2.cvtColor(sct_img, cv2.COLOR_RGB2GRAY)
    else:
        return sct_img


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
templates = []
for image in templates_files:
    image = cv2.imread(image, 0)
    templates.append(image)
threshold = 0.95


def compare_matches(x, y):
    print(x, y)
    return x[3][0] - y[3][0]

ground = 38
	
def extract_features(matches):
	len = np.shape(matches)
	features = np.zeros(8)
	if len == 0:
		features[0] = 1
		features[1] = 1
		features[2] = 0
		features[3] = 0
		features[4] = 1
		features[5] = 1
		features[6] = 0
		features[7] = 0
	elif len == 1:
		object = matches[0]
		features[0] = object[3][0] / grab_areas.get((screen_w, screen_h))[2]
		features[1] = (object[3][1] - ground) / 70
		features[2] = object[1] / 100
		features[3] = (object[3][1] - ground + object[1]) / (grab_areas.get((screen_w, screen_h))[3] * 2)
		features[4] = 1
		features[5] = 1
		features[6] = 0
		features[7] = 0
	else:
		object1 = matches[0]
		object2 = matches[1]
		features[0] = object1[3][0] / grab_areas.get((screen_w, screen_h))[2]
		features[1] = (object1[3][1] - ground) / 70
		features[2] = object1[1] / 100
		features[3] = (object1[3][1] - ground + object1[1]) / (grab_areas.get((screen_w, screen_h))[3] * 2)
		features[4] = object2[3][0] / grab_areas.get((screen_w, screen_h))[2]
		features[5] = (object2[3][1] - ground) / 70
		features[6] = object2[1] / 100
		features[7] = (object2[3][1] - ground + object2[1]) / (grab_areas.get((screen_w, screen_h))[3] * 2)
	return features

def get_matches(screen):
    matches = []
    screen_grey = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    for idx, template in enumerate(templates):
        temp_w, temp_h = template.shape[::-1]  # reversing template size
        res = cv2.matchTemplate(screen_grey, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        coordinates = list(zip(*loc[::-1]))
        print(coordinates)
        for pair in coordinates:
            matches.append((temp_w, temp_h, idx, pair))

    cmp_key = cmp_to_key(compare_matches)
    if matches:
        matches.sort(key=cmp_key)
    print(matches)
    return matches


def draw_screen(screen, detection=False):
    matches = []
    if detection:
        matches = get_matches(screen)
        for match in matches:
            temp_w = match[0]
            temp_h = match[1]
            idx = match[2]
            coordinates = match[3]
            cv2.rectangle(screen, coordinates,
                              (coordinates[0] + temp_w, coordinates[1] + temp_h), colors[idx], 2)

    cv2.imshow('Dino', screen)
    # SHOULD BE PAIRED WITH

    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()
    #     break


