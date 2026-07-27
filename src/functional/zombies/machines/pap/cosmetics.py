""" Rolling a new scope and camo for the weapon leaving the machine. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON


# Functions
def write_pap_cosmetics() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# --- PAP Scope Randomization ---
	# Randomly change the weapon's scope variant when it exits the PAP machine.
	write_versioned_function("zombies/pap/randomize_scope", f"""
data remove storage {ns}:temp _pap_scopes
$data modify storage {ns}:temp _pap_scopes set from storage {ns}:zombies scope_variants."$({BASE_WEAPON})"

# Skip if weapon has no scope variants or only one (default)
execute unless data storage {ns}:temp _pap_scopes[1] run return 0

# Pick a random scope variant using Bookshelf
data modify storage bs:in random.choice.options set from storage {ns}:temp _pap_scopes
function #bs.random:choice
data modify storage {ns}:temp _pap_scope_pick set from storage bs:out random.choice

# Apply the picked scope to the weapon extract
data modify storage {ns}:temp _pap_extract.stats.models.normal set from storage {ns}:temp _pap_scope_pick.model
data modify storage {ns}:temp _pap_extract.stats.models.zoom set from storage {ns}:temp _pap_scope_pick.zoom
data modify storage {ns}:temp _pap_extract.weapon set from storage {ns}:temp _pap_scope_pick.id
data remove storage {ns}:temp _pap_extract.stats.scope_level
execute if data storage {ns}:temp _pap_scope_pick.scope_level run data modify storage {ns}:temp _pap_extract.stats.scope_level set from storage {ns}:temp _pap_scope_pick.scope_level
""")

	# --- PAP Camo Randomization ---
	# Randomly pick a camo variant after scope selection and apply it to the weapon model names.
	write_versioned_function("zombies/pap/randomize_camo", f"""
# MACRO: $({BASE_WEAPON}) from _pap_extract.stats
data modify storage {ns}:temp _pap_camos set value []
$data modify storage {ns}:temp _pap_camos set from storage {ns}:zombies camo_variants."$({BASE_WEAPON})"
execute unless data storage {ns}:temp _pap_camos[0] run data modify storage {ns}:temp _pap_camos set from storage {ns}:zombies camo_variants._default
execute unless data storage {ns}:temp _pap_camos[0] run return 0

# Pick a random camo variant using Bookshelf
data modify storage bs:in random.choice.options set from storage {ns}:temp _pap_camos
function #bs.random:choice
data modify storage {ns}:temp _pap_camo_pick set from storage bs:out random.choice

# Build apply data: post-scope weapon id + picked camo name
data modify storage {ns}:temp _pap_camo_data set value {{}}
data modify storage {ns}:temp _pap_camo_data.camo set from storage {ns}:temp _pap_camo_pick

# Fallback to base weapon id when no scoped weapon id is present
data modify storage {ns}:temp _pap_camo_data.weapon_id set from storage {ns}:temp _pap_extract.stats.{BASE_WEAPON}
execute if data storage {ns}:temp _pap_extract.weapon run data modify storage {ns}:temp _pap_camo_data.weapon_id set from storage {ns}:temp _pap_extract.weapon
function {ns}:v{version}/zombies/pap/apply_camo with storage {ns}:temp _pap_camo_data
""")

	write_versioned_function("zombies/pap/apply_camo", f"""
# MACRO: $(weapon_id) = weapon id after scope selection, $(camo) = camo name
$data modify storage {ns}:temp _pap_extract.stats.models.normal set value "{ns}:$(weapon_id)_$(camo)"
$data modify storage {ns}:temp _pap_extract.stats.models.zoom set value "{ns}:$(weapon_id)_$(camo)_zoom"
""")

	# Set item_model component from scope data
	write_versioned_function("zombies/pap/set_item_model_from_scope", """
$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_model":"$(model)"}}
""")

	# Randomize scope but guarantee a different result than the current one _pap_old_weapon must be set before calling this
	write_versioned_function("zombies/pap/randomize_scope_different", f"""
# Skip if weapon has no scope variants or only one (default)
$data modify storage {ns}:temp _pap_scopes set from storage {ns}:zombies scope_variants."$({BASE_WEAPON})"
execute unless data storage {ns}:temp _pap_scopes[1] run return 0

# Randomize scope again
function {ns}:v{version}/zombies/pap/randomize_scope with storage {ns}:temp _pap_extract.stats

# data modify set returns 0 if values are equal, 1 if different
execute store success score #pap_scope_changed {ns}.data run data modify storage {ns}:temp _pap_old_weapon set from storage {ns}:temp _pap_extract.weapon

# Retry if same weapon ID was picked (guaranteed to terminate since ≥2 variants exist)
execute if score #pap_scope_changed {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/randomize_scope_different
""")

