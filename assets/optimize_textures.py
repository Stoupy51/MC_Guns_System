
# Get start time & Enable colors in Windows 10 console
import os
import time
from typing import cast

from PIL import Image
from stouputils.print import info

START_TIME: float = time.perf_counter()
os.system("color")

# For each texture in the textures folder, optimize it without losing any quality
for root, _, files in os.walk("./"):
	for file in files:
		if not file.endswith(".png"):
			continue
		filepath: str = f"{root}/{file}"

		# Load image
		image = Image.open(filepath).convert("RGBA")
		pixels = image.load()
		if pixels is None:
			continue
		width, height = image.size

		# Optimize image: flatten fully-transparent pixels to (0, 0, 0, 0)
		for x in range(width):
			for y in range(height):
				_r, _g, _b, a = cast(tuple[int, int, int, int], pixels[x, y])
				if a == 0:
					pixels[x, y] = (0, 0, 0, 0)

		# Save image
		image.save(filepath)
		info(f"Optimized '{file}'")

# Total time
total_time: float = time.perf_counter() - START_TIME
info(f"Textures optimized in {total_time:.3f} seconds")
