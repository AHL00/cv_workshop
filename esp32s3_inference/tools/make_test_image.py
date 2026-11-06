"""Convert image.png (next to this script) into the raw RGB888 buffer that the
firmware embeds as main/test_image.rgb.

Usage (needs Pillow):
    python make_test_image.py

Same preprocessing as inference.py: center-crop to the model's aspect ratio,
then resize to the 160x128 (WxH) model input. Also writes test_preview.png
next to this script so you can see exactly what the ESP will receive.
"""
from pathlib import Path
from PIL import Image

W, H = 160, 128

here = Path(__file__).resolve().parent
src = here / "image.png"
dst = here.parent / "main" / "test_image.rgb"
preview = here / "test_preview.png"

img = Image.open(src).convert("RGB")
print(f"source {img.width}x{img.height}")

# Center-crop to the target aspect ratio (no distortion).
target = W / H
if img.width / img.height > target:
    crop_w = int(img.height * target)
    left = (img.width - crop_w) // 2
    img = img.crop((left, 0, left + crop_w, img.height))
else:
    crop_h = int(img.width / target)
    top = (img.height - crop_h) // 2
    img = img.crop((0, top, img.width, top + crop_h))

img = img.resize((W, H), Image.Resampling.BILINEAR)
dst.write_bytes(img.tobytes())  # row-major, R G B per pixel
img.save(preview)
print(f"wrote {dst} ({dst.stat().st_size} bytes) and {preview}")
