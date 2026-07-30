""" Sampling the light around a barricade so its boards match the room's brightness. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_barricade_lighting() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Raise #light to the light level at the current position (exact-match predicates, early exit)
	check_light_lines: str = "".join(
		f"execute if score #light {ns}.data matches ..{level - 1} if predicate {ns}:v{version}/light/{level} run return run scoreboard players set #light {ns}.data {level}\n"
		for level in range(1, 16)
	)
	write_versioned_function("zombies/barricades/check_light", f"""
# Check light level at current position and update #light if higher
{check_light_lines}""")

	## Compute a barricade display's brightness from the light at its position and the 6 neighboring positions (max), instead of the old hardcoded sky/block 15 which made boards glow in dark rooms.
	## @s = barricade display, executed at @s.
	brightness_faces: list[str] = ["~ ~ ~", "~ ~1 ~", "~ ~-1 ~", "~1 ~ ~", "~-1 ~ ~", "~ ~ ~1", "~ ~ ~-1"]
	compute_brightness_lines: str = "".join(
		f"execute if score #light {ns}.data matches ..14 positioned {face} run function {ns}:v{version}/zombies/barricades/check_light\n"
		for face in brightness_faces
	)
	write_versioned_function("zombies/barricades/compute_brightness", f"""
# Reset light score, then sample own position and all 6 neighbors (stop early at 15)
scoreboard players set #light {ns}.data 0
{compute_brightness_lines}
# Apply computed brightness to the display
data merge entity @s {{brightness:{{block:0,sky:0}}}}
execute store result entity @s brightness.block int 1 run scoreboard players get #light {ns}.data
execute store result entity @s brightness.sky int 1 run scoreboard players get #light {ns}.data
""")

	## Single tick dispatch (optimization: ONE @e sweep for all barricade displays)
	write_versioned_function("zombies/barricades/tick", f"""
# @s = barricade display, at @s — dispatch by state
execute if score @s {ns}.zb.barricade.state matches 0 positioned ^ ^ ^-1 run function {ns}:v{version}/zombies/barricades/intact_tick
execute if score @s {ns}.zb.barricade.state matches 1 run function {ns}:v{version}/zombies/barricades/destroyed_tick

# Player collision: push players in barricade's facing direction every tick (both states)
execute as @a[scores={{{ns}.zb.in_game=1}},distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8

# Downed mannequin collision: same push so crawling players can't clip through barricades
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8
""")

