import urllib.request
from rembg import remove
from PIL import Image

import logging
logging.basicConfig(level = logging.INFO)

PICUTRE_PATH_SRC = "./dist/tmp.jpg"
PICTURE_PATH_DST = "./dist/tmp-no-bg.jpg"
PICTURE_PATH_DST_WITH_TICKET = "./dist/tmp-no-bg-ticket.jpg"

TICKET_ASSET_PATH = "./assets/ticket.jpg"

def download_picture(url):
    logging.info(f"Downloading picture from {url}")
    urllib.request.urlretrieve(url, PICUTRE_PATH_SRC)


def superpose_ticket_image():
    logging.info("Adding ticket image to picture")
    bg = Image.open(PICTURE_PATH_DST).convert('RGBA')
    foreground = Image.open(TICKET_ASSET_PATH).convert('RGBA')

    foreground.thumbnail((300,300), Image.Resampling.LANCZOS)
    bg.paste(foreground, ( int(bg.width / 2 - 100), int(bg.height / 2 - 100) ), foreground)
    
    
    bg = bg.convert('RGB')
    bg.save(PICTURE_PATH_DST_WITH_TICKET)
    return bg


def proccess_image():
    logging.info(f"Removing background")
    with open(PICUTRE_PATH_SRC, 'rb') as i:
        with open(PICTURE_PATH_DST, 'wb') as o:
            t = i.read()
            output = remove(t)
            o.write(output)
    logging.info("Background removed")
    
    superpose_ticket_image()
    