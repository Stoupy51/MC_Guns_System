""" Game hooks, the per-round reset and the Carpenter power-up repair. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_barricade_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## One @e sweep for every barricade display.
	write_versioned_function("zombies/game_tick", f"""
# Speeds frozen last tick are restored first.
execute as @e[tag={ns}.zombie_round,tag={ns}.barricade_frozen] run function {ns}:v{version}/zombies/barricades/restore_zombie_speed
execute as @e[type=minecraft:block_display,tag={ns}.barricade_display] at @s run function {ns}:v{version}/zombies/barricades/tick

# Every 5 s, since local light can change (doors, power, placed lights).
scoreboard players add #barricade_bright_timer {ns}.data 1
execute if score #barricade_bright_timer {ns}.data matches 100.. run scoreboard players set #barricade_bright_timer {ns}.data 0
execute if score #barricade_bright_timer {ns}.data matches 0 as @e[type=minecraft:block_display,tag={ns}.barricade_display] at @s run function {ns}:v{version}/zombies/barricades/compute_brightness
""")

	write_versioned_function("zombies/preload_complete", f"""
# Maps saved before the barriers to barricades rename keep the old key, and maps are only appended when missing.
# game.map is a per-game copy, so renaming the key here never touches the stored map.
execute unless data storage {ns}:zombies game.map.barricades if data storage {ns}:zombies game.map.barriers run data modify storage {ns}:zombies game.map.barricades set from storage {ns}:zombies game.map.barriers

execute if data storage {ns}:zombies game.map.barricades[0] run function {ns}:v{version}/zombies/barricades/setup
""")

	write_versioned_function("zombies/barricades/on_round_start", f"""
scoreboard players set @a {ns}.zb.barricade_repairs 0
""", tags=[f"{ns}:zombies/on_round_start"])

	## gm_entity cleanup removes the entities; only tags on living ones remain.
	write_versioned_function("zombies/stop", f"""
tag @e[tag={ns}.barricade_removing] remove {ns}.barricade_removing
tag @a[tag={ns}.barricade_repairing] remove {ns}.barricade_repairing
scoreboard players reset @a {ns}.zb.barricade_repairs
""")

	## Carpenter.
	write_versioned_function("zombies/barricades/repair_all", f"""
execute as @e[type=minecraft:block_display,tag={ns}.barricade_display,scores={{{ns}.zb.barricade.state=1}}] at @s run function {ns}:v{version}/zombies/barricades/instant_repair
""")

	## Run as the barricade display, at it.
	write_versioned_function("zombies/barricades/instant_repair", f"""
scoreboard players set @s {ns}.zb.barricade.state 0

scoreboard players set @s {ns}.zb.barricade.repairing_id 0
scoreboard players set @s {ns}.zb.barricade.removing_id 0

# Release any zombie or player acting on it.
tag @e[tag={ns}.barricade_removing,scores={{{ns}.zb.barricade.removing_id=1..}}] remove {ns}.barricade_removing
tag @a[tag={ns}.barricade_repairing] remove {ns}.barricade_repairing

# Collision and visibility back.
data modify entity @s block_state set from entity @s data.block_enabled

# One slam per barricade: Carpenter reads as the whole map boarded up at once. No budget, it is rare and lasts one tick.
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound {ns}:zombies/barricade/slam block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

