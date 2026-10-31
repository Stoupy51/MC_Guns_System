""" What a zombie or a wolf gets for being one, and the round speed curves of the horde and of the hounds. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function


# Classes
@dataclass(frozen=True)
class RoundSpeed:
	""" A base movement speed from a round on, until the next entry's round. """
	first_round: int
	speed: float


@dataclass(frozen=True)
class EnemyPreset:
	""" Looks and stats a mob of this entity type gets before the map's nbt, which may override any of them. """
	entity: str
	nbt: str
	attack_damage: float
	scale: float


# Constants
PRESETS: list[EnemyPreset] = [
	# Silent: the zombie vocals are played for them (see vocals).
	EnemyPreset(entity="minecraft:zombie", nbt="{Silent:1b}", attack_damage=15.0, scale=1.0),
	# The hound: a black wolf 1.5x the size, biting below a zombie since it reaches you far more often.
	EnemyPreset(entity="minecraft:wolf", nbt='{variant:"minecraft:black"}', attack_damage=12.0, scale=1.5),
]

HORDE_SPEEDS: list[RoundSpeed] = [
	*(RoundSpeed(first_round=round_num, speed=0.19 + round_num / 100) for round_num in range(1, 11)),
	RoundSpeed(first_round=11, speed=0.30),
	RoundSpeed(first_round=30, speed=0.31),
	RoundSpeed(first_round=36, speed=0.32),
]
""" Every enemy but the wolf: +0.01 a round from 0.20, capped at 0.32 from round 36. """

HOUND_SPEEDS: list[RoundSpeed] = [
	RoundSpeed(first_round=1, speed=0.36),
	RoundSpeed(first_round=10, speed=0.40),
	RoundSpeed(first_round=20, speed=0.44),
]
""" Always above the horde's cap: a pack cannot be outrun. """


# Functions
def write_presets() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run as a new enemy, before the map's nbt.
	write_versioned_function("zombies/mob/preset", "\n".join(
		f"execute if entity @s[type={preset.entity}] run return run function {ns}:v{version}/zombies/mob/preset/{preset.entity.split(':')[1]}"
		for preset in PRESETS
	))
	for preset in PRESETS:
		write_versioned_function(f"zombies/mob/preset/{preset.entity.split(':')[1]}", f"""
data merge entity @s {preset.nbt}
attribute @s minecraft:attack_damage base set {preset.attack_damage}
attribute @s minecraft:knockback_resistance base set 1024
{f"attribute @s minecraft:scale base set {preset.scale}" if preset.scale != 1.0 else ""}
""")

	## Run as an enemy after the map's nbt, which this overrides.
	write_versioned_function("zombies/mob/speed", f"""
execute if entity @s[type=minecraft:wolf] run return run function {ns}:v{version}/zombies/mob/speed/hound
{speed_lines(ns, HORDE_SPEEDS)}

# Speed 0.29+ is the BO2 sprint gait, which screams (3-5 s clips) instead of groaning (see vocals).
execute if score #zb_round {ns}.data matches 10.. run tag @s add {ns}.zb_sprint

# From round 15, 10% are walkers (0.20); never a Zonweeb type, whose speed is a factor of the round's.
scoreboard players set #zb_speed_roll {ns}.data 0
execute if score #zb_round {ns}.data matches 15.. if score #zb_type {ns}.data matches 0 store result score #zb_speed_roll {ns}.data run random value 1..10
execute if score #zb_speed_roll {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_speed_roll {ns}.data matches 1 run tag @s remove {ns}.zb_sprint
""")
	write_versioned_function("zombies/mob/speed/hound", speed_lines(ns, HOUND_SPEEDS))


def speed_lines(ns: str, speeds: list[RoundSpeed]) -> str:
	""" One line per entry, setting the base speed for its rounds.

	>>> print(speed_lines("mgs", [RoundSpeed(first_round=1, speed=0.36), RoundSpeed(first_round=10, speed=0.4)]))
	execute if score #zb_round mgs.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
	execute if score #zb_round mgs.data matches 10.. run attribute @s minecraft:movement_speed base set 0.4
	"""
	lines: list[str] = []
	for index, entry in enumerate(speeds):
		lower: str = str(entry.first_round) if index else ""
		upper: str = str(speeds[index + 1].first_round - 1) if index + 1 < len(speeds) else ""
		rounds: str = lower if lower == upper else f"{lower}..{upper}"
		lines.append(f"execute if score #zb_round {ns}.data matches {rounds} run attribute @s minecraft:movement_speed base set {entry.speed:g}")
	return "\n".join(lines)

