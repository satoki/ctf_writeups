import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode


dsas = """\
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　｜　　　　　　｜｜　　｜｜　｜　　｜　　　｜｜　　　　　　｜　　　｜
｜　　　｜｜　　　　｜｜｜｜｜｜　｜　　｜　　　　　｜｜　　　　｜｜　　　｜
｜　　　｜｜｜　　｜｜｜｜｜　　　｜　｜　　｜｜｜｜｜｜｜　　｜｜｜　　　｜
｜　　　｜｜｜　　｜｜｜｜　　｜　　｜　｜　　　｜｜｜｜｜　　｜｜｜　　　｜
｜　　　｜｜｜　　｜｜｜｜　｜　｜｜｜　　｜　　｜｜｜｜｜　　｜｜｜　　　｜
｜　　　｜｜　　　　｜｜　　｜　　　｜　　　｜　｜　｜｜　　　　｜｜　　　｜
｜　　　｜　　　　　　｜｜｜｜｜｜｜｜｜｜｜｜｜｜｜｜　　　　　　｜　　　｜
｜　　　　　　　　　　　｜　　｜｜　　｜　｜　　　｜　　　　　　　　　　　｜
｜　　　　｜｜｜｜｜　｜｜　｜　｜｜　｜　　｜　｜　　｜｜　　　　｜　　　｜
｜　　　｜　　　｜　　　｜　　　　｜　｜｜｜｜　　　　　　｜　　　｜　　　｜
｜　　　　　｜｜｜　　｜｜｜　｜｜｜｜　　　｜｜　　　　｜｜｜　｜　　　　｜
｜　　　　｜　　｜　　　　　｜　　｜　　　　｜　　｜　　　　｜　　｜　　　｜
｜　　　　｜｜　｜｜｜　　｜｜｜　｜｜｜　｜｜｜　｜｜｜　｜｜｜　　　　　｜
｜　　　　　　　｜　｜｜｜　　　　｜　　｜　　　　｜　　｜　　　　　　　　｜
｜　　　　　｜｜｜　　｜｜｜　｜｜｜　｜｜｜　｜｜｜　｜｜｜　｜｜　　　　｜
｜　　　｜｜　　｜　｜｜　　｜　　｜　　｜　｜　｜　｜　｜　｜｜｜｜　　　｜
｜　　　｜｜｜　｜｜　｜　｜｜｜｜　｜　　　　　　｜｜　　｜｜　｜　　　　｜
｜　　　　　　｜｜｜｜　　｜　｜　｜｜　　｜　｜｜｜　　｜｜｜｜｜｜　　　｜
｜　　　｜　｜　｜｜｜｜　｜｜｜｜｜　｜　｜｜｜　｜　｜　｜｜　｜　　　　｜
｜　　　　　｜｜　　　　　｜｜　　｜｜　｜｜　｜｜｜　｜　　｜｜｜｜　　　｜
｜　　　｜｜　｜　　　｜｜｜｜｜　｜｜　　｜　｜｜　　　　｜｜　｜　　　　｜
｜　　　　　　　　　　　｜　　　｜　　　　｜｜　｜｜　　｜｜｜　　｜　　　｜
｜　　　｜　　　　　　｜　｜　｜　　　　　　｜　　｜｜｜｜｜｜｜｜｜　　　｜
｜　　　｜｜　　　　｜｜｜　　｜　　｜｜｜｜　　｜｜　　｜　　｜｜｜　　　｜
｜　　　｜｜｜　　｜｜｜　｜｜　　｜｜｜｜｜　｜｜　　　　｜｜　　｜　　　｜
｜　　　｜｜｜　　｜｜｜｜｜｜　｜　｜　　　｜｜｜｜｜｜　｜｜　｜　　　　｜
｜　　　｜｜｜　　｜｜｜　　｜｜｜｜｜｜｜｜　　｜｜｜｜｜　　｜　　　　　｜
｜　　　｜｜　　　　｜｜｜｜　｜　｜｜｜｜　｜｜　　｜　｜　　　｜　　　　｜
｜　　　｜　　　　　　｜　｜｜　　｜｜　｜　｜｜｜｜｜　　｜｜　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜
｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜\
""".split(
    "\n"
)

qr = []
for line in dsas:
    new_line = []
    now = 0
    for c in line:
        if c == "｜":
            now ^= 255
        new_line.append(now)
    qr.append(new_line[:-1])


qr_array = np.array(qr)
qr_image = Image.fromarray(np.uint8(qr_array))
upscaled_qr_image = qr_image.resize(
    (qr_array.shape[1] * 16, qr_array.shape[0] * 16), Image.Resampling.NEAREST
)

upscaled_qr_image.save("qr.png")

flag = decode(upscaled_qr_image)[0].data.decode("utf-8")
print(flag)
