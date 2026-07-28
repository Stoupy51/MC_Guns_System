""" The command blocks the projectile blast and the grenade blast both run around their damage. """
# Imports
from ...config.stats.keys import EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS


# Classes
class Explosion:
	""" The command blocks the projectile blast and the grenade blast both run around their damage. """

	# Functions
	@staticmethod
	def setup_lines(ns: str, version: str) -> str:
		""" Return the block snapshotting the blast centre, its config and the shooter to credit.

		`@s` is the exploding entity. The centre lands in #ctr_x/y/z as blocks x1000, the config in
		`{ns}:temp expl`, and whoever fired it ends up tagged `{ns}.temp_shooter`.
		The shooter lookup falls back to armed entities because a turret has no player behind it.

		Args:
			ns (str):      The project namespace.
			version (str): The project version.
		Returns:
			str: The commands, one per line, ready to embed in a function body.

		Examples:
			>>> Explosion.setup_lines("mgs", "1.0.0").splitlines()[0]
			'execute store result score #ctr_x mgs.data run data get entity @s Pos[0] 1000'
		"""
		return f"""execute store result score #ctr_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #ctr_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #ctr_z {ns}.data run data get entity @s Pos[2] 1000

# Copy explosion config from entity data to temp storage
data modify storage {ns}:temp expl.{EXPLOSION_DAMAGE} set from entity @s data.config.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp expl.{EXPLOSION_DECAY} set from entity @s data.config.{EXPLOSION_DECAY}
data modify storage {ns}:temp expl.{EXPLOSION_RADIUS} set from entity @s data.config.{EXPLOSION_RADIUS}

# Resolve shooter: copy UUID to storage, then find matching player
data modify storage {ns}:temp expl.shooter_uuid set from entity @s data.shooter

# Tag the matching shooter for damage attribution
scoreboard players set #found {ns}.data 0
execute as @a run function {ns}:v{version}/projectile/match_shooter
execute if score #found {ns}.data matches 0 as @e[tag={ns}.armed] run function {ns}:v{version}/projectile/match_shooter"""

	@staticmethod
	def area_damage_lines(ns: str, version: str) -> str:
		""" Return the call spreading the blast over everything in range, radius read off the entity.

		Args:
			ns (str):      The project namespace.
			version (str): The project version.
		Returns:
			str: Two commands, one per line.

		Examples:
			>>> Explosion.area_damage_lines("mgs", "1.0.0").splitlines()[1]
			'function mgs:v1.0.0/projectile/damage_area with storage mgs:temp expl'
		"""
		return f"""execute store result storage {ns}:temp expl.radius_float float 1 run data get entity @s data.config.{EXPLOSION_RADIUS}
function {ns}:v{version}/projectile/damage_area with storage {ns}:temp expl"""
