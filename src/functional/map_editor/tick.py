""" The editor tick: marker particles and the nearest-element actionbar. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, MODEL_DISPLAY_ELEMENTS


# Functions
def write_editor_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Particles only go to players in editor mode: without a viewer selector a particle command reaches every player on the server.
	editor_viewers: str = f"@a[scores={{{ns}.mp.map_edit=1}},distance=..48]"

	particle_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		# Elements with a real model display need no dust marker.
		if einfo.save_type == "config" or etype in MODEL_DISPLAY_ELEMENTS:
			continue
		r, g, b = einfo.particle
		scale = einfo.particle_scale
		spread = "0.2 0.5 0.2" if einfo.save_type == "spawn" else "0.3 0.5 0.3"
		count = 2 if etype == "base_coordinates" else 1
		particle_lines.append(
			f'execute at @e[type=minecraft:marker,tag={ns}.element.{etype}] run particle dust{{color:[{r},{g},{b}],scale:{scale}}} ~ ~1 ~ {spread} 0 {count} normal {editor_viewers}'
		)

	# Nor the white rotation tick.
	model_excluded: str = "".join(f",tag=!{ns}.element.{etype}" for etype in MODEL_DISPLAY_ELEMENTS)

	actionbar_type_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type == "config":
			continue
		actionbar_type_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run return run title @a[tag={ns}.check_nearest] actionbar [{{"text":"{einfo.emoji} ","color":"{einfo.color}"}},{{"text":"{einfo.name}"}}]'
		)

	# Run as the nearest marker.
	write_versioned_function("maps/editor/actionbar_nearest", "\n".join(actionbar_type_lines))

	write_versioned_function("maps/editor/tick", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Nearest element within 5 blocks; genuinely per player.
tag @s add {ns}.check_nearest
execute as @n[type=minecraft:marker,tag={ns}.map_element,distance=..5] run function {ns}:v{version}/maps/editor/actionbar_nearest
tag @s remove {ns}.check_nearest

# Everything else is map-wide but this runs per editing player, so it is done once per tick, by whoever gets here first.
execute unless score #ed_global_tick {ns}.data = #total_tick {ns}.data run function {ns}:v{version}/maps/editor/global_tick
""")

	## At most once per tick, however many players edit.
	write_versioned_function("maps/editor/global_tick", f"""
# The other editors skip the call above.
scoreboard players operation #ed_global_tick {ns}.data = #total_tick {ns}.data

# Checked once a second and rebuilt only after an edit: syncing a marker's rotation is an NBT read and write, and yaw only changes on edits.
scoreboard players operation #ed_disp_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_disp_phase {ns}.data %= #20 {ns}.data
execute if score #ed_disp_phase {ns}.data matches 0 as @e[type=minecraft:marker,tag={ns}.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if score #ed_disp_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/displays/sync

# Every 4 ticks: dust lingers about a second, so it looks the same with a quarter of the commands and packets.
scoreboard players operation #ed_part_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_part_phase {ns}.data %= #4 {ns}.data
execute if score #ed_part_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/particles
""")

	write_versioned_function("maps/editor/particles", f"""
# Skipped for markers that draw a real model.
execute as @e[type=minecraft:marker,tag={ns}.map_element{model_excluded}] at @s positioned ^ ^ ^0.5 run particle dust{{color:[1.0,1.0,1.0],scale:0.5}} ~ ~1.69 ~ 0.1 0.1 0.1 0 5 normal {editor_viewers}

{chr(10).join(particle_lines)}
""")

