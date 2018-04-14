import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([150, 100, 50])
    upper_red = np.array([180, 255, 180])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    # inRange zwraca 0 lub 1
    res = cv2.bitwise_and(frame, frame, mask=mask)

    kernel = np.ones((15, 15), np.float32) / 225
    smoothed = cv2.filter2D(res, -1, kernel)
    # pokoj był zbyt jasno oświetlony!
    blur = cv2.GaussianBlur(res, (15, 15), 0)

    median = cv2.medianBlur(res, 15)

    bilateral = cv2.bilateralFilter(res, 15, 75, 75)

    cv2.imshow('res', res)
    cv2.imshow('median', median)
    cv2.imshow('res', res)
    cv2.imshow('smoothed', smoothed)
    cv2.imshow('bilateral', bilateral)
    # smoothing - tracimy clarity ale jest troche lepiej
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
