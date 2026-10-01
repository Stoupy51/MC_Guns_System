""" The backup death watch that drops an enemy's weapon. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_drops() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Backup death watch: the weapon drop normally fires from raycast/apply_damage on the killing shot; this catches other deaths (the boundary kill).
	# One entity NBT read per living enemy per tick, as zombies/death_watch_tick: there is no cheaper "did anything die" signal.
	write_versioned_function("missions/death_watch_tick", f"""
execute as @e[tag={ns}.mission_enemy,tag=!{ns}.drop_done] at @s run function {ns}:v{version}/missions/check_enemy_dead
""")

	## Health read into a score, as raycast/apply_damage does: NBT-matching `Health:0.0f` or `DeathTime:1s` never matched in playtests.
	## The sentinel keeps a failed read from reusing the last mob's score.
	write_versioned_function("missions/check_enemy_dead", f"""
scoreboard players set #mi_enemy_hp {ns}.data 1000
execute store result score #mi_enemy_hp {ns}.data run data get entity @s Health 100
execute if score #mi_enemy_hp {ns}.data matches ..0 run function {ns}:v{version}/missions/drop_enemy_weapon
""")

	## Run as the dying enemy, at it. Mobs hold their gun in equipment.mainhand; the rest of the drop is core/weapon_drop.
	write_versioned_function("missions/drop_enemy_weapon", f"""
tag @s add {ns}.drop_done

data remove storage {ns}:temp _dropw
data modify storage {ns}:temp _dropw set from entity @s equipment.mainhand

# Mob guns track no live ammo: 0 makes the drop carry half a magazine, like a player's empty gun.
scoreboard players set #drop_ammo {ns}.data 0
function {ns}:v{version}/shared/drops/drop
""")

