from pathlib import Path
from diffusers import StableDiffusionPipeline
from os import path
from output import save

# what do we want a picture of?
PROMPT = "a skyscraper designed by frank lloyd wright"
SAVE_DIR = "."

# get the huggingface token
def get_token():
    home = path.expanduser("~")
    token_file = path.join(home, ".huggingface", "token")
    token = Path(token_file).read_text()
    return token


# set up pipe
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4", use_auth_token=get_token()
)

# use the GPU
pipe.to("cuda")

# make the image!
image = pipe(PROMPT)["sample"][0]

# save it and send it!
save(image, SAVE_DIR, PROMPT)
