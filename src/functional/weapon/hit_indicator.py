""" BO2-style hit direction indicator: a red arc ringing the crosshair, pointing at the shooter.

One glyph per sector, drawn white and tinted red by the title's text colour.

Minecraft does not centre a glyph on its canvas: it centres the *string* on the sum of the glyphs'
advances, then draws each glyph from that pen position. The advance is measured from content, not
canvas (BitmapProvider.getActualGlyphWidth scans columns from the right for non-zero alpha), so an
arc sitting on the left half reports half the advance and renders off-centre — which is why the
ring used to wander between directions. Every glyph is therefore pinned to the same advance with a
single alpha=1 pixel in a fixed column.
"""
import math

import numpy as np
from beet import Font, Texture
from PIL import Image
from stewbeet import Mem, write_versioned_function

SECTORS: int = 36
""" Directions the indicator can distinguish. Must divide 36000 (yaw range in centidegrees) so the
sector width stays whole: 8, 10, 12, 16, 20, 24, 32, 36 all work. Higher = finer arc, more
textures and commands. """

HIT_DIR_HEIGHT: int = 48
HIT_DIR_ASCENT: int = 20
""" Calibration in font-pixel units (title text renders at 4x GUI scale). HEIGHT is the arc's
screen size, ASCENT shifts it up since the title baseline sits above screen centre. """

CANVAS: int = 256
""" Texture canvas size; the arc is drawn at 2x then downscaled for anti-aliasing. """
ARC_RADIUS: int = 220
""" Outer radius, in 512ths of the canvas size. """
ARC_WIDTH: int = 26
""" Ring thickness, in 512ths of the canvas size. """
ARC_SPAN: float = 90
""" Degrees covered by the arc: two sectors wide. """

GLYPH_CHARS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
""" Codepoints for the sector glyphs; any character works, these need no SNBT/JSON escaping. """

# TODO: Later in 26.3, use post shader new command instead. Do not add it yet.
def main() -> None:
	ns: str = Mem.ctx.project_id
	assert 36000 % SECTORS == 0, f"SECTORS={SECTORS} must divide 36000 (yaw range in centidegrees)"
	assert SECTORS <= len(GLYPH_CHARS), f"SECTORS={SECTORS} exceeds the {len(GLYPH_CHARS)} available glyph chars"

	# Sector 0 = shooter in front (arc at top), clockwise
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:hit_dir", Font({"providers": []}))

	# Pin column solves advance == rendered width, taking the largest valid width so it sits far right.
	# Valid range: (HEIGHT - 1.5) / scale <= actual < (HEIGHT - 0.5) / scale
	scale: float = HIT_DIR_HEIGHT / CANVAS
	pin_column: int = math.ceil((HIT_DIR_HEIGHT - 0.5) / scale) - 2

	# Alpha is per-pixel rather than ImageDraw.arc(), which can only flat-fill, since the arc fades at its ends.
	# Geometry is shared, so the polar grid is built once.
	big: int = CANVAS * 2
	radius: float = ARC_RADIUS * big / 512
	width: float = ARC_WIDTH * big / 512
	yy, xx = np.mgrid[0:big, 0:big]
	centre: float = (big - 1) / 2.0
	dx, dy = xx - centre, yy - centre
	# 0° = 3 o'clock, increasing clockwise (image y axis points down) -> top = -90°
	angle = np.degrees(np.arctan2(dy, dx))
	# Solid core with soft edges; 2.5 widens the plateau so the ring keeps its thickness
	radial = np.clip((1.0 - np.abs(np.hypot(dx, dy) - radius) / (width / 2.0)) * 2.5, 0.0, 1.0)

	for sector in range(SECTORS):
		center_angle: float = -90.0 + (360.0 / SECTORS) * sector
		# Wrapped into -180..180 so the seam at ±180° doesn't cut hard, then faded to transparent
		delta = np.abs((angle - center_angle + 180.0) % 360.0 - 180.0)
		tangential = np.clip(1.0 - delta / (ARC_SPAN / 2.0), 0.0, 1.0)
		rgba = np.empty((big, big, 4), dtype=np.uint8)
		rgba[..., :3] = 255  # White; the title's text colour tints it red at display time
		rgba[..., 3] = (radial * tangential * 255.0).astype(np.uint8)
		img = Image.fromarray(rgba, "RGBA").resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)

		# Pin the advance after the downscale, so resampling cannot wash the marker out
		final = np.array(img)
		content_right: int = int(np.max(np.nonzero(final[..., 3].any(axis=0))))
		assert content_right < pin_column, (
			f"sector {sector} arc reaches column {content_right}, past the advance pin at {pin_column}: "
			f"lower ARC_RADIUS/ARC_WIDTH or raise CANVAS"
		)
		final[0, pin_column, 3] = 1
		img = Image.fromarray(final, "RGBA")

		Mem.ctx.assets.textures[f"{ns}:font/hit_dir_{sector}"] = Texture(img)
		font.data["providers"].append({
			"type": "bitmap",
			"file": f"{ns}:font/hit_dir_{sector}.png",
			"ascent": HIT_DIR_ASCENT,
			"height": HIT_DIR_HEIGHT,
			"chars": [GLYPH_CHARS[sector]],
		})

	# Damage-signal listener (@s = victim); same source detection as the hitmarker listener
	sector_titles: str = "\n".join(
		f'execute if score #hit_dir {ns}.data matches {sector} run title @s title {{"text":"{GLYPH_CHARS[sector]}","font":"{ns}:hit_dir","color":"#FF2A2A"}}'
		for sector in range(SECTORS)
	)
	# Centidegrees, not decidegrees, so sector widths stay whole at any SECTORS (36000/32 = 1125)
	step: int = 36000 // SECTORS
	write_versioned_function("weapon/hit_direction", f"""
# Red {SECTORS}-way hit direction indicator, shown to player victims only
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no meaningful direction (hitscan cannot self-hit)
execute if entity @s[tag={ns}.temp_shooter] run return 0

# Locate the shooter
scoreboard players set #hit_src {ns}.data 0
execute at @s if entity @n[tag={ns}.ticking] run scoreboard players set #hit_src {ns}.data 1
execute at @s if score #hit_src {ns}.data matches 0 if entity @n[tag={ns}.temp_shooter] run scoreboard players set #hit_src {ns}.data 2
execute if score #hit_src {ns}.data matches 0 run return 0

# Yaw toward the shooter (x100): face a scratch marker at the victim toward the shooter, read it back
execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.hit_dir_marker"]}}
execute at @s if score #hit_src {ns}.data matches 1 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.ticking] eyes
execute at @s if score #hit_src {ns}.data matches 2 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.temp_shooter] eyes
execute at @s store result score #hit_dir {ns}.data run data get entity @n[tag={ns}.hit_dir_marker] Rotation[0] 100
execute at @s run kill @n[tag={ns}.hit_dir_marker]

# Sector 0..{SECTORS - 1} relative to the victim's facing (0 = front, clockwise; scoreboard %= is floorMod).
# The half-sector offset makes each sector straddle its direction instead of starting at it.
execute store result score #hit_yaw {ns}.data run data get entity @s Rotation[0] 100
scoreboard players operation #hit_dir {ns}.data -= #hit_yaw {ns}.data
scoreboard players add #hit_dir {ns}.data {step // 2}
scoreboard players operation #hit_dir {ns}.data %= #36000 {ns}.data
scoreboard players operation #hit_dir {ns}.data /= #{step} {ns}.data

# Flash the matching arc glyph around the crosshair (~0.7s, no fade-in)
title @s times 0 8 6
{sector_titles}
""", tags=[f"{ns}:signals/damage"])

