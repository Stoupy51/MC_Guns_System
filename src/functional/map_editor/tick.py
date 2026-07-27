""" The editor tick: marker particles and the nearest-element actionbar. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, MODEL_DISPLAY_ELEMENTS


# Functions
def write_editor_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Editor Tick (universal - shows all element types).
	# Editor particles go only to players actually in editor mode.
	# A particle command with no viewer selector is transmitted to every player on the server, so the markers were costing bandwidth and client FPS for everyone in the game, not just the map maker.
	editor_viewers: str = f"@a[scores={{{ns}.mp.map_edit=1}},distance=..48]"

	particle_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		# Elements with a real model display don't need a dust particle marker
		if einfo.save_type == "config" or etype in MODEL_DISPLAY_ELEMENTS:
			continue
		r, g, b = einfo.particle
		scale = einfo.particle_scale
		spread = "0.2 0.5 0.2" if einfo.save_type == "spawn" else "0.3 0.5 0.3"
		count = 2 if etype == "base_coordinates" else 1
		particle_lines.append(
			f'execute at @e[tag={ns}.element.{etype}] run particle dust{{color:[{r},{g},{b}],scale:{scale}}} ~ ~1 ~ {spread} 0 {count} normal {editor_viewers}'
		)

	# Markers that already draw a real model don't get the white rotation tick either
	model_excluded: str = "".join(f",tag=!{ns}.element.{etype}" for etype in MODEL_DISPLAY_ELEMENTS)

	actionbar_type_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type == "config":
			continue
		actionbar_type_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run return run title @a[tag={ns}.check_nearest] actionbar [{{"text":"{einfo.emoji} ","color":"{einfo.color}"}},{{"text":"{einfo.name}"}}]'
		)

	# Show nearest element name in actionbar (runs as the nearest marker)
	write_versioned_function("maps/editor/actionbar_nearest", "\n".join(actionbar_type_lines))

	write_versioned_function("maps/editor/tick", f"""
# Only run for players in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Actionbar: show nearest element info (within 5 blocks). Genuinely per-player, stays here.
tag @s add {ns}.check_nearest
execute as @n[type=minecraft:marker,tag={ns}.map_element,distance=..5] run function {ns}:v{version}/maps/editor/actionbar_nearest
tag @s remove {ns}.check_nearest

# Everything else the editor draws is map-wide, not per-player, but this function runs once per
# editing player — so marker rotation syncing, the display rebuild and every particle used to be
# repeated for each of them. Do that work once per tick instead, whoever gets here first.
execute unless score #ed_global_tick {ns}.data = #total_tick {ns}.data run function {ns}:v{version}/maps/editor/global_tick
""")

	## Map-wide editor rendering: runs at most once per tick regardless of how many players edit
	write_versioned_function("maps/editor/global_tick", f"""
# Claim this tick so the remaining editors skip straight past the call above
scoreboard players operation #ed_global_tick {ns}.data = #total_tick {ns}.data

# Model displays: rebuild once per second so rotation/config edits on markers stay in sync.
# The marker rotation sync is an NBT read plus an NBT write per marker, which is far too expensive
# to run every tick — and yaw only ever changes when someone edits it, so once a second is plenty.
scoreboard players operation #ed_disp_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_disp_phase {ns}.data %= #20 {ns}.data
execute if score #ed_disp_phase {ns}.data matches 0 as @e[type=minecraft:marker,tag={ns}.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if score #ed_disp_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/refresh_displays

# Marker particles every 4 ticks: dust lingers about a second, so this looks identical to emitting
# them every tick while cutting the particle commands (and the packets they generate) by 4x.
scoreboard players operation #ed_part_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_part_phase {ns}.data %= #4 {ns}.data
execute if score #ed_part_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/particles
""")

	write_versioned_function("maps/editor/particles", f"""
# Rotation indicator, skipped for markers that already draw a real model
execute as @e[type=minecraft:marker,tag={ns}.map_element{model_excluded}] at @s positioned ^ ^ ^0.5 run particle dust{{color:[1.0,1.0,1.0],scale:0.5}} ~ ~1.69 ~ 0.1 0.1 0.1 0 5 normal {editor_viewers}

# Per-element markers
{chr(10).join(particle_lines)}
""")

