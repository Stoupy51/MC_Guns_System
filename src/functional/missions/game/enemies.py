""" The backup death watch that drops an enemy's weapon. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_drops() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Enemy weapon drops.
	# Backup death watch.
	# The drop normally fires from raycast/apply_damage the moment the killing shot lands (@s = victim, gun still in hand); this catches enemies killed by anything that doesn't route through there, e.g. the boundary kill.
	# Cost: one entity-NBT read per living enemy per tick, the same deal zombies pays in zombies/death_watch_tick.
	# There is no cheaper "did anything die" signal to gate it on.
	write_versioned_function("missions/death_watch_tick", f"""
execute as @e[tag={ns}.mission_enemy,tag=!{ns}.drop_done] at @s run function {ns}:v{version}/missions/check_enemy_dead
""")

	## Is this enemy dead?
	## Read the health into a score rather than NBT-matching the corpse: `{Health:0.0f}` and `{DeathTime:1s}` were both tried here and each went 0-for-34 in playtest, while this `data get entity @s Health` read is exactly what raycast/apply_damage uses for kill detection.
	## The sentinel keeps a failed read from reusing the last mob's score.
	write_versioned_function("missions/check_enemy_dead", f"""
scoreboard players set #mi_enemy_hp {ns}.data 1000
execute store result score #mi_enemy_hp {ns}.data run data get entity @s Health 100
execute if score #mi_enemy_hp {ns}.data matches ..0 run function {ns}:v{version}/missions/drop_enemy_weapon
""")

	## Capture step for the shared drop (@s = dying enemy, at its position).
	## Mobs hold their gun in equipment.mainhand instead of an Inventory slot; everything after the capture (ammo bake, spare magazine, ground spawn, pickup) is core/weapon_drop.py.
	write_versioned_function("missions/drop_enemy_weapon", f"""
tag @s add {ns}.drop_done

data remove storage {ns}:temp _dropw
data modify storage {ns}:temp _dropw set from entity @s equipment.mainhand

# Mob guns never track live ammo on a scoreboard: 0 makes the drop carry half a magazine,
# the same deal a player's empty gun leaves behind
scoreboard players set #drop_ammo {ns}.data 0
function {ns}:v{version}/shared/drops/drop
""")

