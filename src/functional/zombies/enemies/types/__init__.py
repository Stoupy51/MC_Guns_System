""" The Zonweeb special types, which replace a plain zombie and scale from the round's. """
# Imports
from dataclasses import dataclass
from itertools import accumulate
from typing import Literal

from stewbeet import Mem, write_versioned_function


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
	armor: str
	""" Material prefix of the full armor set worn ("minecraft:golden" for golden_helmet...), so the type reads from a distance. """
	first_round: int
	weight: int
	""" Percent of the spawns from first_round on. """
	unique: bool = False
	""" At most one alive at a time. """


# Constants
SPECIAL_TYPES: list[ZombieType] = [
	ZombieType(type_id="fast",  speed_percent=125, health_percent=50,  scale=0.85, armor="minecraft:chainmail",  first_round=5,  weight=15),
	ZombieType(type_id="tank",  speed_percent=75,  health_percent=300, scale=1.25, armor="minecraft:netherite",  first_round=10, weight=8),
	ZombieType(type_id="armed", speed_percent=100, health_percent=100, scale=1.0,  armor="minecraft:iron",       first_round=15, weight=5),
	ZombieType(type_id="aura",  speed_percent=90,  health_percent=200, scale=1.15, armor="minecraft:golden",     first_round=20, weight=3, unique=True),
]
""" Rolled in this order (zombies/types/roll): the weights stack into consecutive ranges of 1..100. #zb_type is the index from 1. """

AURA_RADIUS: int = 6
""" Blocks around an aura zombie where the horde takes Resistance II. """


# Functions
def write_enemy_types() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	type_rolls: str = "\n".join(
		f"execute if score #zb_type_roll {ns}.data matches {upper - zombie.weight + 1}..{upper} if score #zb_round {ns}.data matches {zombie.first_round}.. "
		+ (f"unless entity @e[type=minecraft:zombie,tag={ns}.zb_{zombie.type_id},limit=1] " if zombie.unique else "")
		+ f"run scoreboard players set #zb_type {ns}.data {index}"
		for index, (zombie, upper) in enumerate(zip(SPECIAL_TYPES, accumulate(z.weight for z in SPECIAL_TYPES), strict=True), start=1)
	)
	## Run as a plain zombie being built; #zb_type stays 0 unless a type comes up.
	write_versioned_function("zombies/types/roll", f"""
execute store result score #zb_type_roll {ns}.data run random value 1..100
{type_rolls}
""")

	## Run as the zombie once the round scaled it.
	write_versioned_function("zombies/types/apply", "\n".join(
		f"execute if score #zb_type {ns}.data matches {index} run return run function {ns}:v{version}/zombies/types/{zombie.type_id}"
		for index, zombie in enumerate(SPECIAL_TYPES, start=1)
	))

	for zombie in SPECIAL_TYPES:
		# No armor points, which would cut every hit and undo health_percent; unbreakable so hits never strip it.
		armor_lines: str = "\n".join(
			f"item replace entity @s armor.{slot} with {zombie.armor}_{piece}[attribute_modifiers=[],unbreakable={{}}]"
			for slot, piece in (("head", "helmet"), ("chest", "chestplate"), ("legs", "leggings"), ("feet", "boots"))
		)
		write_versioned_function(f"zombies/types/{zombie.type_id}", f"""
tag @s add {ns}.zb_{zombie.type_id}

# {zombie.speed_percent}% of the round's speed; the escort taxi reads this base value.
execute store result storage {ns}:temp _zb_speed.value double {zombie.speed_percent / 100000} run attribute @s minecraft:movement_speed base get 1000
function {ns}:v{version}/zombies/set_speed with storage {ns}:temp _zb_speed
execute store result score #zb_speed {ns}.data run attribute @s minecraft:movement_speed base get 1000
execute if score #zb_speed {ns}.data matches 290.. run tag @s add {ns}.zb_sprint
execute if score #zb_speed {ns}.data matches ..289 run tag @s remove {ns}.zb_sprint

# {zombie.health_percent}% of the health the round just gave (#zb_hp).
scoreboard players operation #zb_hp {ns}.data *= #{zombie.health_percent} {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #100 {ns}.data
execute if score #zb_hp {ns}.data matches 3073.. run scoreboard players set #zb_hp {ns}.data 3072
function {ns}:v{version}/zombies/apply_zombie_hp

attribute @s minecraft:scale base set {zombie.scale}
{armor_lines}
data modify entity @s drop_chances set value {{head:0f,chest:0f,legs:0f,feet:0f}}
""")

	# The gun comes from the enemy build, like a spawn's armed mob; its 5% Max Ammo drop is in on_zombie_dying.
	write_versioned_function("zombies/types/armed", f"""
data modify storage {ns}:temp _mob.gun set value {{}}
""")

	write_versioned_function("zombies/set_speed", """
$attribute @s minecraft:movement_speed base set $(value)
""")

	## Once a second; the 2 s effect bridges the gap and lapses on its own once the aura zombie dies.
	write_versioned_function("zombies/aura_tick", f"""
effect give @e[type=minecraft:zombie,tag={ns}.zombie_round,distance=..{AURA_RADIUS}] minecraft:resistance 2 1 true
particle minecraft:soul_fire_flame ~ ~1 ~ {AURA_RADIUS / 2} 0.5 {AURA_RADIUS / 2} 0 12 normal
""")

