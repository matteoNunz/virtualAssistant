import os
import subprocess as sp
import cv2 as cv2

# Set the paths to the programs the assistant must be able to open
paths = {
    'notepad': "C:\\Windows\\system32\\notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}


def open_notepad():
    """
    Method used to open the notepad
    :return: nothing
    """
    os.startfile(paths['notepad'])


def open_cmd():
    """
    Method used to open the command line or prompt
    :return: nothing
    """
    os.system('start cmd')


def open_camera():
    """
    Method used to open the camera (webcam)
    :return: nothing
    """
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    """
    Method used to open the calculator
    :return: nothing
    """
    sp.Popen(paths['calculator'])


def logout():
    """
    Method used to logout from the account (it will close all the open application)
    :return: nothing
    """
    os.system("shutdown /l")


def take_photo():
    """
    Method used to take a picture
    :return: nothing, but save the image in the folder
    """
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
    