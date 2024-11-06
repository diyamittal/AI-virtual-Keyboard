import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
from pynput.keyboard import Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["<---"]]
finalText = ""

keyboard = Controller()

def drawALL(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (70, 70, 70), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text




buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key != "<---":
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
            buttonList.append(Button([280, 450], "Space", [300, 85]))
            space_pressed = False
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, size=[200, 85]))

#buttonList.append(Button([50, 500], "Space", [300, 85]))

space_pressed = False

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    lmList1 = None
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]

    img = drawALL(img, buttonList)

    space_pressed = False

    if lmList1:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if button.text != "<---":
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                            4, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)
                    print(l)

                    if l < 30:
                        if button.text == "Space" and not space_pressed:
                            finalText += " "
                            space_pressed = True
                            sleep(0.15)
                        elif button.text != "Space":
                            keyboard.press(button.text)
                            keyboard.release(button.text)
                            finalText += button.text
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4,
                                                            (86, 255, 255), 4)
                            sleep(0.15)

            else:
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4,
                                                    (255, 255, 255), 4)

                    p1 = lmList1[8][:2]
                    p2 = lmList1[12][:2]
                    l, _, _ = detector.findDistance(p1, p2, img)
                    print(l)

                    if l < 30:
                        # Remove last character from finalText
                        finalText = finalText[:-1]
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4,
                                                        (86, 255, 255), 4)
                        sleep(0.15)

    cv2.rectangle(img, (50, 650), (1035, 550), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, finalText, (60, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
