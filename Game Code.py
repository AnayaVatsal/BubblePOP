import cv2
import numpy as np
import mediapipe as mp
import math
import random
import time
import datetime
import pygame
import sys


# initialize pygame
pygame.init()

# setting up webcam feed
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# using mediapipe to detect hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


class Circle:  # initialize and draw circles in webcam feed
    def __init__(self, coordinates, radius, color, thickness):
        self.coordinates = coordinates
        self.radius = radius
        self.color = color
        self.thickness = thickness

    def draw_circle(self, frame_name):
        cv2.circle(frame_name, self.coordinates, self.radius, self.color, self.thickness)


# center circle to begin game
target = Circle((int(1280/2), int(720/2)), 50, (186, 172, 49), -1)

# set score
score_value = 0

# set game run time
seconds = 3000


# define timer to set time in seconds?
def timer():
    pass


def audio():
    pygame.mixer.init()
    pygame.mixer.music.load('track.mp3')
    pygame.mixer.music.play()


def collision(radius_hand_circle, radius_target):  # condition for collision of hand circle with the target circle
    dist = math.sqrt((target.coordinates[0] - cen_x) ** 2 + (target.coordinates[1] - cen_y) ** 2)
    if dist <= radius_hand_circle + radius_target:
        target.color = (0, 255, 0)
        global score_value
        score_value += 1
        audio()

    if dist > radius_hand_circle + radius_target:
        target.color = (186, 172, 49)


def random_target():  # spawn random target
    if target.color == (0, 255, 0):
        target.coordinates = (random.randrange(0, 1266), random.randrange(0, 696))


while True:  # main game loop
    # read camera feed
    ret, frame = cam.read()
    # flip video from camera
    flipped_cam = cv2.flip(frame, flipCode=1)
    # convert to RGB
    RGB_frame = cv2.cvtColor(flipped_cam, cv2.COLOR_BGR2RGB)
    target.draw_circle(flipped_cam)

    if ret:  # if camera captures video then proceed
        # detecting hands
        result = hands.process(RGB_frame)
        if result.multi_hand_landmarks:  # for when multiple hands are detected
            for hand_landmarks in result.multi_hand_landmarks:
                # mp_drawing.draw_landmarks(flipped_cam, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # use the above line of code to mark the landmarks in hand

                # x and y coordinates of the hand
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                y_coords = [landmark.y for landmark in hand_landmarks.landmark]

                # find center of hand
                cen_x = int(sum(x_coords) / len(x_coords) * flipped_cam.shape[1])
                cen_y = int(sum(y_coords) / len(y_coords) * flipped_cam.shape[0])

                # draw circle at all hands detected by using the Circle class
                hand_circle = Circle((cen_x, cen_y), 50, (109, 255, 175), 5)
                hand_circle.draw_circle(flipped_cam)
                if seconds > 0:
                    seconds -= 1

                # call the collision function to check for collision of hand circle and the target
                collision(hand_circle.radius, target.radius)

                # once the center target is hit spawn random targets
                random_target()

        # adding text on the screen
        cv2.putText(flipped_cam, "Pop the Bubbles!", (350, 60),
                    cv2.FONT_ITALIC, 2, (0, 0, 0), 3)

        cv2.putText(flipped_cam, "Press 'q' to return to the main menu", (650, 700),
                    cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

        cv2.putText(flipped_cam, "Score : " + str(score_value), (10, 25),
                    cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

        cv2.putText(flipped_cam, "Time left : " + str(seconds), (10, 55),
                    cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

        # displaying the window
        cv2.imshow("GAME", flipped_cam)

        # condition to exit the window
        if cv2.waitKey(1) & 0xFF == ord("q") or seconds == 0:
            break

cam.release()
cv2.destroyAllWindows()

# set up screen to display score
score_screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Score')

# score levels
if score_value >= 70:
    remarks = 'Excellent Score :D TRY TO BEAT THE HIGH SCORE'
elif score_value >= 50:
    remarks = 'Great Score :) TRY ONCE MORE'
elif score_value >= 30:
    remarks = 'Good Score :) TRY ONCE MORE'
elif score_value > 0:
    remarks = 'Average Score -_- TRY AGAIN '
else:
    remarks = 'Zero?! :( TRY AGAIN '

# text display on screen
font1 = pygame.font.SysFont('Roboto', 60)
player_score = font1.render('Score = ' + str(score_value), True, 'white')
player_score_rect = player_score.get_rect(center=(400, 200))

font2 = pygame.font.SysFont('Roboto', 40)
score_remarks = font2.render('' + remarks, False, 'purple ')
score_remarks_rect = player_score.get_rect(center=(130, 400))


# loop for score screen
a = True
while a:
    score_screen.fill((240, 200, 250))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False

    score_screen.blit(player_score, player_score_rect)
    score_screen.blit(score_remarks, score_remarks_rect)
    pygame.display.update()
pygame.quit()