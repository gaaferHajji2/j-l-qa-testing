from PIL import Image

img = Image.open('tomatoes.jpg')
print(f"size: {img.size}")
print(f"format: {img.format}")
print(f"mode: {img.mode}")