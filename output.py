import re
from PIL import Image
from io import BufferedReader
import requests
import os
import path

USER_KEY = os.environ["PUSHOVER_USER_KEY"]
APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]

# Send image data to pushover with a message string
def sendToPushover(imageBytes: BufferedReader, filename: str, message: str):
    r = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={"token": APP_TOKEN, "user": USER_KEY, "message": message},
        files={"attachment": (filename, imageBytes, "image/png")},
        # files={"attachment": ("image.jpg", open("your_image.jpg", "rb"), "image/jpeg")},
    )
    return r.text


def save(image: Image, dir: str, description: str) -> None:
    filename = re.sub(r"[^a-zA-Z]+", "-", description) + ".png"
    filepath = path.join(dir, filename)
    image.save(filepath)
    # it's weirdly difficult to turn this image into byte data.
    # one of the easiest ways is just to re-read the file from the filesystem
    imageBytes = open(filepath, "rb")
    sendToPushover(imageBytes, filename, description)
