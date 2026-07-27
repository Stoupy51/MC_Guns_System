""" Assembling the lore array for a gun or a grenade, then writing it onto the item. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.colors import END_HEX


# Functions
def write_lore_build() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Build gun lore (macro function, called with storage mgs:input lore)
	write_versioned_function("lore/build_gun", f"""
# Initialize new lore array
data modify storage {ns}:temp new_lore set value []

# -- Damage Per Bullet --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates damage
$data modify storage {ns}:temp lore_line append value "$(damage)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Ammo Remaining (X/Y) --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates ammo
$data modify storage {ns}:temp lore_line append value "$(remaining)"
data modify storage {ns}:temp lore_line append value {{"text":"/","color":"#{END_HEX}"}}
$data modify storage {ns}:temp lore_line append value "$(capacity)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Reloading Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates reload
$data modify storage {ns}:temp lore_line append value "$(reload_int).$(reload_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Fire Rate (optional, only if the weapon has a cooldown) --
execute if score #has_cooldown {ns}.data matches 1 run function {ns}:v{version}/lore/append_fire_rate_line with storage {ns}:input lore

# -- Pellets Per Shot (optional, only for shotguns) --
execute if score #has_pellets {ns}.data matches 1 run function {ns}:v{version}/lore/append_pellet_line with storage {ns}:input lore

# -- Damage Decay --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates decay
$data modify storage {ns}:temp lore_line append value "$(decay_pct)"
data modify storage {ns}:temp lore_line append value {{"text":"%","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Switch Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates switch_time
$data modify storage {ns}:temp lore_line append value "$(switch_int).$(switch_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Empty separator (compound, not bare "" — keeps lore NBT homogeneous, see EMPTY_LORE_LINE) --
data modify storage {ns}:temp new_lore append value {{"text":"","italic":false}}
""")

	# Append fire rate line (separate function for conditional execution; unit depends on rate)
	write_versioned_function("lore/append_fire_rate_line", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates fire_rate
$data modify storage {ns}:temp lore_line append value "$(rate_int).$(rate_dec) "
execute if score #fire_rate_tenths {ns}.data matches 10.. run data modify storage {ns}:temp lore_line append from storage {ns}:lore_templates fire_rate_sps
execute if score #fire_rate_tenths {ns}.data matches ..9 run data modify storage {ns}:temp lore_line append from storage {ns}:lore_templates fire_rate_spshot
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Append pellet line (separate function for conditional execution)
	write_versioned_function("lore/append_pellet_line", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates pellets
$data modify storage {ns}:temp lore_line append value "$(pellets)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Build grenade lore (macro function)
	write_versioned_function("lore/build_grenade", f"""
# Initialize new lore array
data modify storage {ns}:temp new_lore set value []

# -- Type --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates grenade_type
$data modify storage {ns}:temp lore_line append value "$(type_display)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Explosion Damage (optional) --
execute if score #has_expl_damage {ns}.data matches 1 run function {ns}:v{version}/lore/append_expl_damage with storage {ns}:input lore

# -- Explosion Radius (optional) --
execute if score #has_expl_radius {ns}.data matches 1 run function {ns}:v{version}/lore/append_expl_radius with storage {ns}:input lore

# -- Fuse Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates grenade_fuse
$data modify storage {ns}:temp lore_line append value "$(fuse_int).$(fuse_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Empty separator (compound, not bare "" — keeps lore NBT homogeneous, see EMPTY_LORE_LINE) --
data modify storage {ns}:temp new_lore append value {{"text":"","italic":false}}
""")

	# Append explosion damage line
	write_versioned_function("lore/append_expl_damage", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates expl_damage
$data modify storage {ns}:temp lore_line append value "$(expl_damage)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Append explosion radius line
	write_versioned_function("lore/append_expl_radius", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates expl_radius
$data modify storage {ns}:temp lore_line append value "$(expl_radius)"
data modify storage {ns}:temp lore_line append value {{"text":" blocks","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Apply new lore to item
	write_versioned_function("lore/apply", f"""
# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag={ns}.update_lore] $(slot)

# Replace lore with rebuilt version
data modify entity @s item.components."minecraft:lore" set from storage {ns}:temp new_lore

# Copy modified item back to player
$item replace entity @p[tag={ns}.update_lore] $(slot) from entity @s contents

# Clean up
kill @s
""")

