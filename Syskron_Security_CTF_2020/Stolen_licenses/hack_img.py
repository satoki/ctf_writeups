import cv2
import pyocr
from PIL import Image

# https://ja.wikipedia.org/wiki/Luhnアルゴリズム より
def check_number(digits):
    _sum = 0
    alt = False
    for d in reversed(digits):
        d = int(d)
        assert 0 <= d <= 9
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        _sum += d
        alt = not alt
    return (_sum % 10) == 0

i = 1
while True:
    img = cv2.imread("B999582-{}.png".format(str(i).zfill(4)))
    img = img[450:500, 100:700]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("test.png", img)
    tools = pyocr.get_available_tools()
    tool = tools[0]
    img = Image.open("test.png")
    key = tool.image_to_string(img, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=6))
    if check_number(key.replace(" ","")):
        print("B999582-{}.png".format(str(i).zfill(4)))
        print(key)
        break
    else:
        print(i)
    i += 1