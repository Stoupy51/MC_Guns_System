""" The PaP-room lure marker and the sweep that sends escorts toward it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_tag, write_versioned_function

from .shared import MAX_ESCORTS, PAP_ROOM_RADIUS


# Functions
def write_escort_lure() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# PaP-room lure
	write_tag("zombies/setup_lure", Mem.ctx.data[ns].function_tags, [])
	write_versioned_function("zombies/escort/setup_lure_center", f"""
kill @e[tag={ns}.lure_center]

# Let the map place its lure centre marker, run positioned at the map base
execute store result storage {ns}:temp _base.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _base.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _base.z int 1 run scoreboard players get #gm_base_z {ns}.data
data modify storage {ns}:temp _base.fn set value "#{ns}:zombies/setup_lure"
function {ns}:v{version}/shared/call_at_base with storage {ns}:temp _base

# Enable the lure only if the map actually placed a centre marker (its opt-in)
scoreboard players set #zb_pap_has {ns}.data 0
execute if entity @e[tag={ns}.lure_center] run scoreboard players set #zb_pap_has {ns}.data 1
scoreboard players set #zb_lure {ns}.data 0
""")

	# Lure is on only when at least one player is alive and every alive player is in the PaP room
	write_versioned_function("zombies/escort/update_lure", f"""
execute store result score #zb_lure_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
scoreboard players set #zb_lure_inpap {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] at @s if entity @e[type=minecraft:interaction,tag={ns}.pap_machine,distance=..{PAP_ROOM_RADIUS}] run scoreboard players add #zb_lure_inpap {ns}.data 1

scoreboard players set #zb_lure {ns}.data 0
execute if score #zb_lure_alive {ns}.data matches 1.. if score #zb_lure_inpap {ns}.data = #zb_lure_alive {ns}.data run scoreboard players set #zb_lure {ns}.data 1

# Start center-bound escorts on a few stray zombies while luring (cap-gated; the retarget in
# escort/start reads #zb_lure and aims at the centre marker)
execute if score #zb_lure {ns}.data matches 1 if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,tag=!{ns}.zb_escort_failed,limit=2,sort=random] at @s unless entity @e[tag={ns}.lure_center,distance=..16] run function {ns}:v{version}/zombies/escort/start
""")

