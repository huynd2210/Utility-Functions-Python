import hashlib
import re
import time

import cv2
import keyboard
import easyocr
import numpy as np
import pyautogui
import pynput
import json


def initEasyOCR():
    reader = easyocr.Reader(['en'])
    return reader

def readTextOnScreenGivenRegion(startX, startY, width, height, ocrReadingFunction, **kwargs):
    #Screenshot the region
    pyautogui.screenshot("temp.png", region=(startX, startY, width, height))

    #Read the image
    result = ocrReadingFunction("temp.png", **kwargs)
    return result

def removeNonCharactersExceptWhitespaceAndNumbers(input_string):
    # Replace all non-characters except whitespace with an empty string
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_string)


def remove_extra_whitespaces(input_string):
    # Replace multiple whitespaces with a single whitespace
    return re.sub(r'\s+', ' ', input_string).strip()

def pressAutoServe():
    print("Auto serve ready")
    while True:
        targetPixelColor = (5, 84, 76)
        targetCoordinatesX, targetCoordinatesY = 400, 980
        actualPixelColor = pyautogui.pixel(targetCoordinatesX, targetCoordinatesY)

        if actualPixelColor == targetPixelColor:
            print("Auto Serve button pressed")
            pressButton('ctrl')



        time.sleep(0.3)


def pressButtonKeyboard(button, delay=0.04):
    keyboard.press(button)
    time.sleep(delay)
    keyboard.release(button)

def pressButton(button, delay=0.047, isDebug=True):
    if button == '':
        return

    if isDebug:
        print("Pressing button: ", button)
    # pyautogui.press(button)
    pressButtonKeyboard(button)
    time.sleep(delay)

def isColorSameWithinThreshold(color1, color2, threshold=10):
    print(color1, color2)
    print("Differences are: ", abs(color1[0] - color2[0]), abs(color1[1] - color2[1]), abs(color1[2] - color2[2]))
    isColorSame = abs(color1[0] - color2[0]) < threshold and abs(color1[1] - color2[1]) < threshold and abs(color1[2] - color2[2]) < threshold
    print("Is color same: ", isColorSame)
    return isColorSame

def removeNumbers(s):
    return ''.join([i for i in s if not i.isdigit()])
def triggerFunctionUponKeypress(triggerKey, function, **kwargs):
    print("Waiting for keypress...")
    while True:
        if keyboard.is_pressed(triggerKey):
            print("triggered")
            function(**kwargs)

#kwargs need to be the same for all functions
def multipleTriggerUponKeypress(triggerFunctionMap, **kwargs):
    print("Waiting for keypress...")
    while True:
        for triggerKey in triggerFunctionMap.keys():
            if keyboard.is_pressed(triggerKey):
                print("triggered")
                triggerFunctionMap[triggerKey](**kwargs)

def getPixelColor(*args):
    if len(args) == 1 and isinstance(args[0], (tuple, list)):
        x, y = args[0]
    elif len(args) == 2:
        x, y = args
    else:
        raise ValueError("Invalid arguments. Use either getPixelColor(x, y) or getPixelColor((x, y)).")
    return pyautogui.pixel(x, y)


def isColorPresentInImage(image_path, target_color, tolerance=0):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the target color to a NumPy array
    target_color_np = np.array(target_color)

    # Calculate the Euclidean distance between each pixel color and the target color
    distances = np.linalg.norm(image_rgb - target_color_np, axis=2)

    # Check if any pixel is within the specified tolerance
    if np.any(distances <= tolerance):
        return True

    return False

def isColorPresentInRegionOnScreen(target_color, region, tolerance=0):
    # Read the image
    pyautogui.screenshot("temp.png", region=region)
    return isColorPresentInImage("temp.png", target_color, tolerance)
def generateImageHash(image_path):
    with open(image_path, "rb") as f:
        # Read the binary data of the image
        image_data = f.read()
        # Create an MD5 hash object
        md5_hash = hashlib.md5()
        # Update the hash object with the image data
        md5_hash.update(image_data)
        # Get the hexadecimal representation of the hash
        hashed_image = md5_hash.hexdigest()

        return hashed_image

def appendCache(ocrCache, imagePath, value, persistCache=True):
    hashedImage = generateImageHash(imagePath)
    ocrCache[hashedImage] = value
    if persistCache:
        saveImageOCRCacheToFile(ocrCache)
def checkCache(ocrCache, imagePath):
    hashedImage = generateImageHash(imagePath)
    return ocrCache[hashedImage] if hashedImage in ocrCache else None

def loadOCRCache(filePath="ocrCache.json"):
    try:
        with open(filePath, 'r') as file:
            ocrCache = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty dictionary
        ocrCache = {}
    return ocrCache

def saveImageOCRCacheToFile(ocrCache, filePath="ocrCache.json"):
    try:
        with open(filePath, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty dictionary
        existing_data = {}

    existing_data.update(ocrCache)

    with open(filePath, 'w') as file:
        json.dump(existing_data, file, indent=4)

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")

def getCoordinatesOnMouseClick():
    # Set up the listener
    print("Ready for mouse clicks")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
