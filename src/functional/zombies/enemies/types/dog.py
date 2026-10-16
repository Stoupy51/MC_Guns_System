""" Hellhounds: the round's zombie health on a faster, weaker-biting body. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_dog_type() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/types/dog", f"""
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# Same HP as the round's zombie: dogs threaten through speed and damage.
function {ns}:v{version}/zombies/calc_zombie_hp
scoreboard players operation @s {ns}.zb.max_hp = #zb_hp {ns}.data

# A modifier, not a base value: every save/load round-trip (any /data modify or `store result entity`) runs
# TamableAnimal.setTame(false, true), which resets the MAX_HEALTH base of an untamed wolf to 8.
scoreboard players remove #zb_hp {ns}.data 8
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_dog_hp with storage {ns}:temp _zb_hp
function {ns}:v{version}/zombies/absorb_above_cap

# Always above the zombie cap (0.32): a dog pack cannot be outrun.
execute if score #zb_round {ns}.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round {ns}.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round {ns}.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Below zombie melee (15.0), since dogs reach you far more often.
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# 1.5x a vanilla wolf, which also enlarges the hitbox.
attribute @s minecraft:scale base set 1.5
""")

