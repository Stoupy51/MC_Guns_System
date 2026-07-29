""" Items and functions the three modes hand out identically. """
# Imports
from stewbeet import Mem, write_versioned_function


# Classes
class SharedContent:
	""" Items and functions the three modes hand out identically. """

	# Functions
	@staticmethod
	def knife_item_snbt(ns: str, short_range: bool = False) -> str:
		""" The melee knife item, shared by zombies (hotbar.0) and multiplayer (hotbar.0).

		Args:
			ns          (str):  The project namespace.
			short_range (bool): Clamp the wielder's entity interaction range down to melee distance.
				Guns hit at whatever range their raycast reaches, so multiplayer wants the knife to be
				an explicit close-quarters trade; zombies keeps vanilla reach for its starting knife.

		Returns:
			str: The item SNBT, ready for `item replace entity @s <slot> with <this>`.
		"""
		modifiers: list[str] = [
			'{type:"movement_speed",amount: 0.1,operation:"add_multiplied_base",slot:"mainhand",id:"minecraft:base_movement_speed"}',
			'{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}',
			'{type:"attack_speed",amount:-2.5,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_speed"}',
		]
		if short_range:
			# Vanilla entity interaction range is 3; add_value of -1.0 leaves 2.0 blocks of reach
			modifiers.append(
				f'{{type:"entity_interaction_range",amount:-1.0,operation:"add_value",slot:"mainhand",id:"{ns}:knife_range"}}'
			)
		# item_model points at the `combat_knife` DB item's model; the item itself stays inline
		# because multiplayer needs the short_range variant that the DB entry does not carry.
		return (
			f"minecraft:iron_sword[unbreakable={{}},custom_data={{{ns}:{{knife:true,combat_knife:true}}}},"
			f"item_model=\"{ns}:combat_knife\","
			f'item_name={{"text":"Knife","color":"white","italic":false}},'
			f"attribute_modifiers=[{','.join(modifiers)}]"
			f"]"
		)

	@staticmethod
	def write_shared_projectile_functions() -> None:
		""" Write shared mcfunctions used by both projectile and grenade systems. """
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		from ...config.stats.keys import PROJECTILE_SPEED

		# Calculate velocity from the look direction, apply it to bs.vel, then teleport back.
		# Requires @s at the summon position with data.config.PROJECTILE_SPEED set.
		# Spread comes from raycast/accuracy/apply_spread.
		write_versioned_function("shared/calc_velocity", f"""
# Record current position for teleporting back later
execute store result score #proj_ox {ns}.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz {ns}.data run data get entity @s Pos[2] 1000

# Apply accuracy spread to the rotation
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Get direction vector by teleporting from origin
execute positioned 0.0 0.0 0.0 positioned ^ ^ ^1 run tp @s ~ ~ ~

# Read direction as velocity components (thousandths of a block)
execute store result score @s bs.vel.x run data get entity @s Pos[0] 1000
execute store result score @s bs.vel.y run data get entity @s Pos[1] 1000
execute store result score @s bs.vel.z run data get entity @s Pos[2] 1000

# Multiply direction by speed / 1000 to get velocity
execute store result score #proj_speed {ns}.data run data get entity @s data.config.{PROJECTILE_SPEED}
scoreboard players operation @s bs.vel.x *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.y *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.z *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.x /= #1000 {ns}.data
scoreboard players operation @s bs.vel.y /= #1000 {ns}.data
scoreboard players operation @s bs.vel.z /= #1000 {ns}.data

# Teleport back to original position
execute store result storage {ns}:temp _tp_pos.x double 0.001 run scoreboard players get #proj_ox {ns}.data
execute store result storage {ns}:temp _tp_pos.y double 0.001 run scoreboard players get #proj_oy {ns}.data
execute store result storage {ns}:temp _tp_pos.z double 0.001 run scoreboard players get #proj_oz {ns}.data
function {ns}:v{version}/shared/tp_back with storage {ns}:temp _tp_pos
""")

		# Shared: Teleport back to original position (macro)
		write_versioned_function("shared/tp_back",
	"""
$tp @s $(x) $(y) $(z)
""")

