from PIL import Image
from PIL import ImageEnhance

img = Image.open('rose1.png')

test_enhance = ImageEnhance.Sharpness(img)
test_enhance.enhance(100.0).save('sharp_rose1.png')