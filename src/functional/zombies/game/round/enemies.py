""" Per-type enemy setup and the Treyarch health curve behind it. """
# Imports
from dataclasses import dataclass
from typing import Literal

from stewbeet import Mem, write_versioned_function


# Classes
@dataclass(frozen=True)
class ZombieType:
	""" A Zonweeb special zombie, scaled from the round's normal zombie, which it replaces at spawn. """
	type_id: Literal["fast", "tank"]
	speed_percent: int
	health_percent: int
	""" Of the BO health curve, still capped at 2048. """
	scale: float
	""" Body size, so the type reads from across a room. """
	first_round: int
	weight: int
	""" Percent of the spawns from first_round on. """


# Constants
SPECIAL_TYPES: list[ZombieType] = [
	ZombieType(type_id="fast", speed_percent=125, health_percent=50,  scale=0.85, first_round=5,  weight=15),
	ZombieType(type_id="tank", speed_percent=75,  health_percent=300, scale=1.25, first_round=10, weight=8),
]
""" Rolled in this order at spawn (zombies/do_spawn_zombie): the weights stack into consecutive ranges of 1..100. """


# Functions
def write_enemy_types() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Each enemy type takes {level:"1".."4"}; the armed stub falls through to the normal scaling.

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

# From round 15, 10% are walkers (0.20); never a special type, whose speed is a factor of the round's.
scoreboard players set #zb_speed_roll {ns}.data 0
execute if score #zb_round {ns}.data matches 15.. unless score #zb_no_walker {ns}.data matches 1 store result score #zb_speed_roll {ns}.data run random value 1..10
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

	for zombie in SPECIAL_TYPES:
		write_versioned_function(f"zombies/types/{zombie.type_id}", f"""
scoreboard players set #zb_no_walker {ns}.data 1
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
scoreboard players set #zb_no_walker {ns}.data 0
tag @s add {ns}.zb_{zombie.type_id}

# {zombie.speed_percent}% of the round's speed; the escort taxi reads this base value.
execute store result storage {ns}:temp _zb_speed.value double {zombie.speed_percent / 100000} run attribute @s minecraft:movement_speed base get 1000
function {ns}:v{version}/zombies/set_speed with storage {ns}:temp _zb_speed
execute store result score #zb_speed {ns}.data run attribute @s minecraft:movement_speed base get 1000
execute if score #zb_speed {ns}.data matches 290.. run tag @s add {ns}.zb_sprint
execute if score #zb_speed {ns}.data matches ..289 run tag @s remove {ns}.zb_sprint

# {zombie.health_percent}% of the health normal just applied (#zb_hp).
scoreboard players operation #zb_hp {ns}.data *= #{zombie.health_percent} {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #100 {ns}.data
execute if score #zb_hp {ns}.data matches 2049.. run scoreboard players set #zb_hp {ns}.data 2048
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

attribute @s minecraft:scale base set {zombie.scale}
""")

	write_versioned_function("zombies/set_speed", """
$attribute @s minecraft:movement_speed base set $(value)
""")

