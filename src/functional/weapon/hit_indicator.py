
# Imports
import math

import numpy as np
from beet import Font, Texture
from PIL import Image
from stewbeet import Mem, write_versioned_function

# BO2-style hit direction indicator: a red arc ringing the crosshair, pointing toward the shooter.
# One glyph per sector, drawn white and tinted red by the title's text color.

# How many directions the indicator can distinguish. Must divide 36000 (the yaw range in centidegrees)
# so the sector width stays a whole number: 8, 10, 12, 16, 20, 24, 32, 36... all work.
# Higher values mean a finer arc and more textures/commands (one of each per sector).
SECTORS: int = 36

# Calibration constants (font-pixel units; title text renders at 4x GUI scale).
# Tweak these until the arc rings the crosshair in-game: HEIGHT is the arc's screen size,
# ASCENT shifts it up (title baseline sits slightly above screen center).
HIT_DIR_HEIGHT: int = 48
HIT_DIR_ASCENT: int = 20

# Texture geometry (drawn at 2x then downscaled for anti-aliasing)
CANVAS: int = 256
ARC_RADIUS: int = 220         # outer radius, in 512ths of the canvas size
ARC_WIDTH: int = 26           # ring thickness, in 512ths of the canvas size
ARC_SPAN: float = 90          # degrees covered by the arc: two sectors wide

# Codepoints for the sector glyphs. Any character works (the font is only ever used by this one
# title), but these are the ones that need no escaping in SNBT or JSON.
GLYPH_CHARS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


# TODO: Later in 26.3, use post shader new command instead. Do not add it yet.
def main() -> None:
	ns: str = Mem.ctx.project_id
	assert 36000 % SECTORS == 0, f"SECTORS={SECTORS} must divide 36000 (yaw range in centidegrees)"
	assert SECTORS <= len(GLYPH_CHARS), f"SECTORS={SECTORS} exceeds the {len(GLYPH_CHARS)} available glyph chars"

	# Generate the arc textures: sector 0 = shooter in front (arc at top), clockwise.
	# PIL arc angles: 0° = 3 o'clock, increasing clockwise (y axis points down) -> top = -90°.
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:hit_dir", Font({"providers": []}))

	# Minecraft does not centre a glyph on its canvas: it centres the *string* on the sum of the
	# glyphs' advances, then draws each glyph from that pen position across its full canvas width.
	# And the advance is measured from the content, not the canvas -- BitmapProvider.getActualGlyphWidth
	# scans columns from the right and stops at the first one holding a non-zero alpha, so a glyph whose
	# arc sits on the left half reports half the advance and gets drawn a quarter-canvas off-centre.
	# That is why the ring wandered between directions.
	#
	# Fix: pin every glyph to the same advance with a single alpha=1 pixel in a fixed column, so all
	# sectors measure identically. The column is chosen so the resulting advance equals the glyph's
	# rendered width exactly, which lands the canvas centre on the string centre rather than half a
	# pixel beside it. Solving advance == rendered width, i.e.
	#     floor(0.5 + actual * scale) + 1 == canvas * scale == HIT_DIR_HEIGHT
	# gives a whole range of valid widths: (HEIGHT - 1.5) / scale <= actual < (HEIGHT - 0.5) / scale.
	# Take the largest one, so the pin sits as far right as possible and leaves the most clearance for
	# the arc (a low HIT_DIR_HEIGHT widens each font pixel, pulling the range down into the artwork).
	scale: float = HIT_DIR_HEIGHT / CANVAS
	pin_column: int = math.ceil((HIT_DIR_HEIGHT - 0.5) / scale) - 2

	# Alpha is computed per-pixel rather than with ImageDraw.arc(), which can only flat-fill: the arc
	# has to fade out toward its two ends, and (softly) at its inner/outer edges. Geometry is shared
	# by all sectors, so the polar grid is built once and only the angular term varies below.
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

	for sector in range(SECTORS):
		center_angle: float = -90.0 + (360.0 / SECTORS) * sector
		# Signed angular distance from the arc's centre, wrapped into -180..180 so the seam at ±180°
		# doesn't produce a hard cut, then faded linearly to fully transparent at both ends.
		delta = np.abs((angle - center_angle + 180.0) % 360.0 - 180.0)
		tangential = np.clip(1.0 - delta / (ARC_SPAN / 2.0), 0.0, 1.0)
		rgba = np.empty((big, big, 4), dtype=np.uint8)
		rgba[..., :3] = 255  # white; the title's text colour tints it red at display time
		rgba[..., 3] = (radial * tangential * 255.0).astype(np.uint8)
		img = Image.fromarray(rgba, "RGBA").resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)

		# Pin the advance (see above). Done after the downscale so the resampling can't wash the
		# marker out, and only once it is certain no arc pixel already sits further right.
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

	# Damage-signal listener: @s = victim. Hitscan shooters carry {ns}.ticking during their tick,
	# explosion shooters {ns}.temp_shooter (same source detection as the hitmarker listener).
	sector_titles: str = "\n".join(
		f'execute if score #hit_dir {ns}.data matches {sector} run title @s title {{"text":"{GLYPH_CHARS[sector]}","font":"{ns}:hit_dir","color":"#FF2A2A"}}'
		for sector in range(SECTORS)
	)
	# Yaw is read in centidegrees (x100) rather than decidegrees so that sector widths stay whole
	# numbers at any SECTORS value (36000/32 = 1125, whereas 3600/32 would not divide).
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

