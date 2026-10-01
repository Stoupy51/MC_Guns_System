""" Per-type enemy setup and the Treyarch health curve behind it. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_types() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Each enemy type takes {level:"1".."4"}; stubs fall through to the normal scaling.

	## Normal zombie: scale health and speed, then start the rise.
	write_versioned_function("zombies/types/normal", f"""
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# BO1 curve: +100 BO HP per round until round 9, then x1.1 per round.
function {ns}:v{version}/zombies/calc_zombie_hp
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

# Capped at 0.32 from round 36.
execute if score #zb_round {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round {ns}.data matches 2 run attribute @s minecraft:movement_speed base set 0.21
execute if score #zb_round {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.22
execute if score #zb_round {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round {ns}.data matches 5 run attribute @s minecraft:movement_speed base set 0.24
execute if score #zb_round {ns}.data matches 6 run attribute @s minecraft:movement_speed base set 0.25
execute if score #zb_round {ns}.data matches 7 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_round {ns}.data matches 8 run attribute @s minecraft:movement_speed base set 0.27
execute if score #zb_round {ns}.data matches 9 run attribute @s minecraft:movement_speed base set 0.28
execute if score #zb_round {ns}.data matches 10 run attribute @s minecraft:movement_speed base set 0.29
execute if score #zb_round {ns}.data matches 11..29 run attribute @s minecraft:movement_speed base set 0.30
execute if score #zb_round {ns}.data matches 30..35 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round {ns}.data matches 36.. run attribute @s minecraft:movement_speed base set 0.32

# Speed 0.29+ is the BO2 sprint gait, which screams (3-5 s clips) instead of groaning (see vocals).
execute if score #zb_round {ns}.data matches 10.. run tag @s add {ns}.zb_sprint

# From round 15, 10% are walkers (0.20).
execute if score #zb_round {ns}.data matches 15.. store result score #zb_speed_roll {ns}.data run random value 1..10
execute if score #zb_round {ns}.data matches 15.. if score #zb_speed_roll {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round {ns}.data matches 15.. if score #zb_speed_roll {ns}.data matches 1 run tag @s remove {ns}.zb_sprint

# 7.5 hearts, no knockback.
attribute @s minecraft:attack_damage base set 15.0
attribute @s minecraft:knockback_resistance base set 1024

# 20 ticks to rise 2 blocks.
scoreboard players set @s {ns}.zb.rise_tick 20
""")

	## Treyarch BO1 HP curve: 50 + 100 x round up to round 9 (150 to 950), then 950 x 1.1^(round - 9),
	## converted with 2/15 (BO 150 HP = 20 HP, a vanilla zombie).
	write_versioned_function("zombies/calc_zombie_hp", f"""
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data *= #100 {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players add #zb_hp {ns}.data 50

execute if score #zb_round {ns}.data matches 10.. run scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run scoreboard players remove #zb_exp_round {ns}.data 9

execute if score #zb_round {ns}.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round {ns}.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run function #bs.math:pow
execute if score #zb_round {ns}.data matches 10.. store result score #zb_hp {ns}.data run data get storage bs:out math.pow 950

scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data

# Also catches int overflow on very high rounds.
execute unless score #zb_hp {ns}.data matches 15..2048 run scoreboard players set #zb_hp {ns}.data 2048
""")

	write_versioned_function("zombies/apply_zombie_hp", """
$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
""")

	## Dogs: $(val) is the amount above a wolf's base 8, as a modifier the taming reset cannot clear (see types/dog).
	write_versioned_function("zombies/apply_dog_hp", f"""
$attribute @s minecraft:max_health modifier add {ns}:dog_hp $(val) add_value
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
""")

	write_versioned_function("zombies/types/dog", f"""
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# Same HP as the round's zombie: dogs threaten through speed and damage.
function {ns}:v{version}/zombies/calc_zombie_hp

# A modifier, not a base value: every save/load round-trip (any /data modify or `store result entity`) runs
# TamableAnimal.setTame(false, true), which resets the MAX_HEALTH base of an untamed wolf to 8.
scoreboard players remove #zb_hp {ns}.data 8
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_dog_hp with storage {ns}:temp _zb_hp

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

	## Armed zombie stub.
	write_versioned_function("zombies/types/armed", f"""
# TODO: ranged attack, drops an ammo power-up on death.
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Fast zombie stub.
	write_versioned_function("zombies/types/fast", f"""
# TODO: higher movement speed, less health.
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Tank zombie stub.
	write_versioned_function("zombies/types/tank", f"""
# TODO: very high health, slow movement.
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

