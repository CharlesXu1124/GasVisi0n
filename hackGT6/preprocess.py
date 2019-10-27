
import urllib.request
from PIL import Image, ImageDraw

URL = 'https://i.pinimg.com/originals/89/b5/71/89b5716381ce485bfae7b6ee6dbd4d4b.jpg'

with urllib.request.urlopen(URL) as url:
    with open('temp.jpg', 'wb') as f:
        f.write(url.read())

img = Image.open('temp.jpg')
draw = ImageDraw.Draw(im)

img.show()
