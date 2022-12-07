import urllib.request
from rembg import remove

import logging
logging.basicConfig(level = logging.INFO)

PICUTRE_PATH_SRC = "./dist/tmp.jpg"
PICTURE_PATH_DST = "./dist/tmp-no-bg.jpg"

def download_picture(url):
    logging.info(f"Downloading picture from {url}")
    urllib.request.urlretrieve(url, PICUTRE_PATH_SRC)


def proccess_image():
    logging.info(f"Removing background")
    with open(PICUTRE_PATH_SRC, 'rb') as i:
        with open(PICTURE_PATH_DST, 'wb') as o:
            t = i.read()
            output = remove(t)
            o.write(output)
    logging.info("Background removed")
