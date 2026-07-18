
# Imports
from beet import Font, Texture
from PIL import Image, ImageDraw
from stewbeet import Mem, write_versioned_function

# BO2-style hit direction indicator: a red arc ringing the crosshair, pointing toward the shooter.
# 8 glyphs (A..H), one per 45° sector, drawn white and tinted red by the title's text color.

# Calibration constants (font-pixel units; title text renders at 4x GUI scale).
# Tweak these until the arc rings the crosshair in-game: HEIGHT is the arc's screen size,
# ASCENT shifts it up (title baseline sits slightly above screen center).
HIT_DIR_HEIGHT: int = 56
HIT_DIR_ASCENT: int = 33

# Texture geometry (drawn at 2x then downscaled for anti-aliasing)
CANVAS: int = 512
ARC_RADIUS: int = 220        # outer radius at 512px canvas
ARC_WIDTH: int = 26          # ring thickness
ARC_SPAN: int = 90           # degrees covered by the arc


def main() -> None:
	ns: str = Mem.ctx.project_id

	# Generate the 8 arc textures: sector 0 = shooter in front (arc at top), clockwise.
	# PIL arc angles: 0° = 3 o'clock, increasing clockwise (y axis points down) -> top = -90°.
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:hit_dir", Font({"providers": []}))
	for sector in range(8):
		big: int = CANVAS * 2
		img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		margin: int = big // 2 - ARC_RADIUS * 2
		center_angle: int = -90 + 45 * sector
		draw.arc(
			(margin, margin, big - margin, big - margin),
			start=center_angle - ARC_SPAN // 2, end=center_angle + ARC_SPAN // 2,
			fill=(255, 255, 255, 255), width=ARC_WIDTH * 2,
		)
		img = img.resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)
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

