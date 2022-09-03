import re
import requests
import flickrapi
from PIL import Image
from io import BufferedReader, BytesIO
from os import environ, path

PUSHOVER_USER_KEY = environ["PUSHOVER_USER_KEY"]
PUSHOVER_APP_TOKEN = environ["PUSHOVER_APP_TOKEN"]

FLICKR_APP_KEY = environ["FLICKR_APP_KEY"]
FLICKR_APP_SECRET = environ["FLICKR_APP_SECRET"]


def uploadToFlickr(filepath: str, title: str, description: str):
    api = flickrapi.FlickrAPI(FLICKR_APP_KEY, FLICKR_APP_SECRET)

    if not api.token_valid():
        # OOB: out of band
        api.get_request_token(oauth_callback="oob")

        verifier = str(
            input(
                f"Get verifier code from {api.auth_url(perms='write')} and enter it here.\n: "
            )
        )

        # Get access token and store it as ${HOME}/.flickr/oauth-tokens.sqlite.
        # If you want to remove the cache, call api.token_cache.forget().
        api.get_access_token(verifier)
        # res is instance of xml.etree.ElementTree.Element.
    # This element has something like "<rsp><photoid>1234</photoid></rsp>".
    res = api.upload(
        filename=filepath,
        title=title,
        description=description,
        is_private=True,
    )
    print(res)


# Send image data to pushover with a message string
def sendToPushover(imageBytes: BufferedReader, filename: str, message: str):
    r = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_APP_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "message": message,
        },
        files={"attachment": (filename, imageBytes, "image/png")},
    )
    print(r.text)


def output(image: Image, dir: str, description: str) -> None:
    trimmedDescription = description[0:20]
    filename = re.sub(r"[^a-zA-Z]+", "-", trimmedDescription) + ".png"
    filepath = path.join(dir, filename)
    image.save(filepath)

    uploadToFlickr(
        filepath,
        title=trimmedDescription,
        description=description,
    )
