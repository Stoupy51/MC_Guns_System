""" Blocks the hitscan raycast and projectiles pass straight through. """
# Imports
from stewbeet import Mem, write_tag


# Functions
def write_raycast_tags() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Write empty block tag (blocks fully ignored by the hitscan raycast; includes barrier so invisible map boundaries never reduce damage or stop bullets)
	write_tag(f"{ns}:v{version}/empty", Mem.ctx.data.block_tags, values=[
		"minecraft:air",
		"minecraft:cave_air",
		"minecraft:void_air",
		"minecraft:light",
		"minecraft:structure_void",
		"minecraft:barrier",
	])

	# Blocks projectiles fly through (bs.move ignored_blocks): everything the default allows, plus barrier so invisible map boundaries never stop rockets/ray gun shots
	write_tag(f"{ns}:v{version}/projectile_pass_through", Mem.ctx.data.block_tags, values=[
		"#bs.hitbox:can_pass_through",
		"minecraft:barrier",
	])

