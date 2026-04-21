from PIL import Image
import os

img = "rose1.png"
f, ext = os.path.splitext(img)
outfile = f + ".jpg"

if img != outfile:
    try:
        with Image.open(img) as t1:
            png_img = t1.convert('RGB')
            png_img.save(outfile)
    except OSError as e: 
        print(f"Can't convert, err is: {e}")