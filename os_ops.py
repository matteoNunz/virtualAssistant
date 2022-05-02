import os
import subprocess as sp
import cv2 as cv2

paths = {
    'notepad': "C:\\Windows\\system32\\notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}


def open_notepad():
    os.startfile(paths['notepad'])


def open_cmd():
    os.system('start cmd')


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])


def logout():
    os.system("shutdown /l")


def take_photo():
    # Select the cam -> 0 is the webcam
    cam_port = 0
    cam = cv2.VideoCapture(cam_port, cv2.CAP_ANY)

    # Reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error, show result
    if result:
        # Showing result, it takes frame name and image output
        cv2.imshow("PictureTest", image)

        # Saving image in local storage
        cv2.imwrite("PictureTest.jpg", image)
    else:
        print("No image detected. Please! try again")
    