""" The zombie types: the normal reference, and the Zonweeb special types scaled from it. """
# Imports
from dataclasses import dataclass
from typing import Literal

from stewbeet import Mem, write_versioned_function

from .curve import write_health_curve
from .dog import write_dog_type


# Classes
@dataclass(frozen=True)
class ZombieType:
	""" A Zonweeb special zombie, scaled from the round's normal zombie, which it replaces at spawn. """
	type_id: Literal["fast", "tank", "armed", "aura"]
	speed_percent: int
	health_percent: int
	""" Of the BO health curve, still capped at 3072 (see apply_zombie_hp). """
	scale: float
	""" Body size, so the type reads from across a room. """
	head: str
	""" Skull worn on the head, so the type reads from a distance whatever the body size. """
	first_round: int
	weight: int
	""" Percent of the spawns from first_round on. """
	unique: bool = False
	""" At most one alive at a time. """


# Constants
SPECIAL_TYPES: list[ZombieType] = [
	ZombieType(type_id="fast",  speed_percent=125, health_percent=50,  scale=0.85, head="minecraft:creeper_head", first_round=5,  weight=15),
	ZombieType(type_id="tank",  speed_percent=75,  health_percent=300, scale=1.25, head="minecraft:wither_skeleton_skull", first_round=10, weight=8),
	ZombieType(type_id="armed", speed_percent=100, health_percent=100, scale=1.0,  head="minecraft:piglin_head", first_round=15, weight=5),
	ZombieType(type_id="aura",  speed_percent=90,  health_percent=200, scale=1.15, head="minecraft:dragon_head", first_round=20, weight=3, unique=True),
]
""" Rolled in this order at spawn (zombies/do_spawn_zombie): the weights stack into consecutive ranges of 1..100. """

AURA_RADIUS: int = 6
""" Blocks around an aura zombie where the horde takes Resistance II. """


# Functions
def write_enemy_types() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	write_health_curve()
	write_dog_type()

	# Each enemy type takes {level:"1".."4"}.

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

	# The Missions gun AI: a random weapon, a visible name, and shots at the nearest player (mob/tick).
	# Its 5% Max Ammo drop is in on_zombie_dying.
	armed_setup: str = f'$function {ns}:v{version}/mob/default/on_new {{entity:"Zombie",level:$(level),active_time:60,sleep_time:40}}'
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
execute if score #zb_hp {ns}.data matches 3073.. run scoreboard players set #zb_hp {ns}.data 3072
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

attribute @s minecraft:scale base set {zombie.scale}
item replace entity @s armor.head with {zombie.head}
data modify entity @s drop_chances.head set value 0f
{armed_setup if zombie.type_id == "armed" else ""}
""")

	write_versioned_function("zombies/set_speed", """
$attribute @s minecraft:movement_speed base set $(value)
""")

	## Once a second; the 2 s effect bridges the gap and lapses on its own once the aura zombie dies.
	write_versioned_function("zombies/aura_tick", f"""
effect give @e[type=minecraft:zombie,tag={ns}.zombie_round,distance=..{AURA_RADIUS}] minecraft:resistance 2 1 true
particle minecraft:soul_fire_flame ~ ~1 ~ {AURA_RADIUS / 2} 0.5 {AURA_RADIUS / 2} 0 12 normal
""")

