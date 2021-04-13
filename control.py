import cv2
import numpy as np
import pyautogui

#open the video camera 0 -> internal camera
capture = cv2.VideoCapture(0)

#create a loop to keep the camera open

#detection of objects with a specific color
#for more accuracy we'll use the range of a color(available in cv2)
#i'll use yellow

yellow_lower = np.array([22, 93, 0])
yellow_upper = np.array([45, 255, 255])

prev_y = 0
while True:
    #retrieve -> not so important
    #frame -> central part
    retrieve, frame = capture.read()

    # creating a mask (highlighting what we want to detect)
    # gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            x, y, width, height = cv2.boundingRect(c)
            #cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0,100,0), 2)
            if y > prev_y:
                pyautogui.press('down')
                print("Moving down")
            elif y < prev_y:
                pyautogui.press('up')
            prev_y = y

    #display the image (name of the frame will be the name of the dialog)
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #use q to close the connection with the camera
    if cv2.waitKey(10) == ord('q'):
        break

#cleanup
capture.release()

#multiple running apps destroyed
cv2.destroyAllWindows()
