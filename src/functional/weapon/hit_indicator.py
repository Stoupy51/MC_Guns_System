
# Imports
import numpy as np
from beet import Font, Texture
from PIL import Image
from stewbeet import Mem, write_versioned_function

# BO2-style hit direction indicator: a red arc ringing the crosshair, pointing toward the shooter.
# 8 glyphs (A..H), one per 45° sector, drawn white and tinted red by the title's text color.

# Calibration constants (font-pixel units; title text renders at 4x GUI scale).
# Tweak these until the arc rings the crosshair in-game: HEIGHT is the arc's screen size,
# ASCENT shifts it up (title baseline sits slightly above screen center).
HIT_DIR_HEIGHT: int = 56
HIT_DIR_ASCENT: int = 33

# Texture geometry (drawn at 2x then downscaled for anti-aliasing)
CANVAS: int = 256
ARC_RADIUS: int = 220        # outer radius, in 512ths of the canvas size
ARC_WIDTH: int = 26          # ring thickness, in 512ths of the canvas size
ARC_SPAN: int = 90           # degrees covered by the arc

# TODO: Later in 26.3, use post shader new command instead. Do not add it yet.
def main() -> None:
	ns: str = Mem.ctx.project_id

	# Generate the 8 arc textures: sector 0 = shooter in front (arc at top), clockwise.
	# PIL arc angles: 0° = 3 o'clock, increasing clockwise (y axis points down) -> top = -90°.
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:hit_dir", Font({"providers": []}))

	# Alpha is computed per-pixel rather than with ImageDraw.arc(), which can only flat-fill: the arc
	# has to fade out toward its two ends, and (softly) at its inner/outer edges. Geometry is shared
	# by all 8 sectors, so the polar grid is built once and only the angular term varies below.
	big: int = CANVAS * 2
	radius: float = ARC_RADIUS * big / 512
	width: float = ARC_WIDTH * big / 512
	yy, xx = np.mgrid[0:big, 0:big]
	centre: float = (big - 1) / 2.0
	dx, dy = xx - centre, yy - centre
	# 0° = 3 o'clock, increasing clockwise (image y axis points down) -> top = -90°, matching sectors.
	angle = np.degrees(np.arctan2(dy, dx))
	# Radial profile: a solid core with soft edges. The 2.5 factor widens the plateau so the ring keeps its
	# thickness instead of reading as a thin blur; the clip is what anti-aliases the edges.
	radial = np.clip((1.0 - np.abs(np.hypot(dx, dy) - radius) / (width / 2.0)) * 2.5, 0.0, 1.0)

	for sector in range(8):
		center_angle: float = -90.0 + 45.0 * sector
		# Signed angular distance from the arc's centre, wrapped into -180..180 so the seam at ±180°
		# doesn't produce a hard cut, then faded linearly to fully transparent at both ends.
		delta = np.abs((angle - center_angle + 180.0) % 360.0 - 180.0)
		tangential = np.clip(1.0 - delta / (ARC_SPAN / 2.0), 0.0, 1.0)
		rgba = np.empty((big, big, 4), dtype=np.uint8)
		rgba[..., :3] = 255  # white; the title's text colour tints it red at display time
		rgba[..., 3] = (radial * tangential * 255.0).astype(np.uint8)
		img = Image.fromarray(rgba, "RGBA").resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)
		Mem.ctx.assets.textures[f"{ns}:font/hit_dir_{sector}"] = Texture(img)
		font.data["providers"].append({
			"type": "bitmap",
			"file": f"{ns}:font/hit_dir_{sector}.png",
			"ascent": HIT_DIR_ASCENT,
			"height": HIT_DIR_HEIGHT,
			"chars": [chr(ord("A") + sector)],
		})

	# Damage-signal listener: @s = victim. Hitscan shooters carry {ns}.ticking during their tick,
	# explosion shooters {ns}.temp_shooter (same source detection as the hitmarker listener).
	sector_titles: str = "\n".join(
		f'execute if score #hit_dir {ns}.data matches {sector} run title @s title {{"text":"{chr(ord("A") + sector)}","font":"{ns}:hit_dir","color":"#FF2A2A"}}'
		for sector in range(8)
	)
	write_versioned_function("weapon/hit_direction", f"""
# Red 8-way hit direction indicator, shown to player victims only
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no meaningful direction (hitscan cannot self-hit)
execute if entity @s[tag={ns}.temp_shooter] run return 0

# Locate the shooter
scoreboard players set #hit_src {ns}.data 0
execute at @s if entity @n[tag={ns}.ticking] run scoreboard players set #hit_src {ns}.data 1
execute at @s if score #hit_src {ns}.data matches 0 if entity @n[tag={ns}.temp_shooter] run scoreboard players set #hit_src {ns}.data 2
execute if score #hit_src {ns}.data matches 0 run return 0

# Yaw toward the shooter (x10): face a scratch marker at the victim toward the shooter, read it back
execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.hit_dir_marker"]}}
execute at @s if score #hit_src {ns}.data matches 1 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.ticking] eyes
execute at @s if score #hit_src {ns}.data matches 2 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.temp_shooter] eyes
execute at @s store result score #hit_dir {ns}.data run data get entity @n[tag={ns}.hit_dir_marker] Rotation[0] 10
execute at @s run kill @n[tag={ns}.hit_dir_marker]

# Sector 0..7 relative to the victim's facing (0 = front, clockwise; scoreboard %= is floorMod)
execute store result score #hit_yaw {ns}.data run data get entity @s Rotation[0] 10
scoreboard players operation #hit_dir {ns}.data -= #hit_yaw {ns}.data
scoreboard players add #hit_dir {ns}.data 225
scoreboard players operation #hit_dir {ns}.data %= #3600 {ns}.data
scoreboard players operation #hit_dir {ns}.data /= #450 {ns}.data

# Flash the matching arc glyph around the crosshair (~0.7s, no fade-in)
title @s times 0 8 6
{sector_titles}
""", tags=[f"{ns}:signals/damage"])

