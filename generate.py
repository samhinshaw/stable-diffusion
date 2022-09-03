from PIL import Image
from pathlib import Path
from diffusers import StableDiffusionPipeline
from os import path
from output import output
import torch

# what do we want a picture of?
# PROMPT = "photograph portrait osama bin laden by platon"
prompts = [
    "portrait of Bugs Bunny by Leonardo da Vinci",
    "portrait of Bugs Bunny by Monet",
    "portrait of Bugs Bunny by Rembrant",
    "portrait of Bugs Bunny by Frida Kahlo",
    "portrait of Bugs Bunny by Picasso",
    "portrait of Bugs Bunny by Vermeer",
    "portrait of Bugs Bunny by Cezanne",
    "portrait of Bugs Bunny by Andy Warhol",
    "portrait of Bugs Bunny by Caravaggio",
]
SAVE_DIR = "results"

# get the huggingface token
def get_token():
    home = path.expanduser("~")
    token_file = path.join(home, ".huggingface", "token")
    token = Path(token_file).read_text()
    return token


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


def generate_grid(prompts: list[str] | str) -> Image:
    all_images = []
    for prompt in prompts:
        with torch.autocast("cuda"):
            image = [generate(prompt)]
        all_images.extend(image)

    grid = image_grid(all_images, rows=3, cols=3)
    return grid


def generate(prompt: str) -> Image:
    # set up pipe
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        use_auth_token=get_token(),
    )

    pipe.to("cuda")

    # generator = torch.Generator("cuda").manual_seed(1026)
    image = pipe(
        prompt,
        height=512,
        width=512,
        guidance_scale=6,  # generator=generator
    )["sample"][0]
    return image


image = generate_grid(prompts)
# save it to disk and upload the results!
output(image, SAVE_DIR, description="\n ".join(prompts))
