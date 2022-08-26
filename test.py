from pathlib import Path
from diffusers import StableDiffusionPipeline
from os import path

# what do we want a picture of?
prompt = "a skyscraper designed by frank lloyd wright"


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
image = pipe(prompt)["sample"][0]
image.save(f"result.png")
