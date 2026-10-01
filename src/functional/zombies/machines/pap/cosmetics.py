""" Rolling a new scope and camo for the weapon leaving the machine. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON


# Functions
def write_pap_cosmetics() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Random scope variant on the way out of the machine.
	write_versioned_function("zombies/pap/randomize_scope", f"""
data remove storage {ns}:temp _pap_scopes
$data modify storage {ns}:temp _pap_scopes set from storage {ns}:zombies scope_variants."$({BASE_WEAPON})"

# Nothing to pick with fewer than 2 variants.
execute unless data storage {ns}:temp _pap_scopes[1] run return 0

data modify storage bs:in random.choice.options set from storage {ns}:temp _pap_scopes
function #bs.random:choice
data modify storage {ns}:temp _pap_scope_pick set from storage bs:out random.choice

data modify storage {ns}:temp _pap_extract.stats.models.normal set from storage {ns}:temp _pap_scope_pick.model
data modify storage {ns}:temp _pap_extract.stats.models.zoom set from storage {ns}:temp _pap_scope_pick.zoom
data modify storage {ns}:temp _pap_extract.weapon set from storage {ns}:temp _pap_scope_pick.id
data remove storage {ns}:temp _pap_extract.stats.scope_level
execute if data storage {ns}:temp _pap_scope_pick.scope_level run data modify storage {ns}:temp _pap_extract.stats.scope_level set from storage {ns}:temp _pap_scope_pick.scope_level
""")

	# Random camo on top of the picked scope.
	write_versioned_function("zombies/pap/randomize_camo", f"""
# Macro: $({BASE_WEAPON}) from _pap_extract.stats.
data modify storage {ns}:temp _pap_camos set value []
$data modify storage {ns}:temp _pap_camos set from storage {ns}:zombies camo_variants."$({BASE_WEAPON})"
execute unless data storage {ns}:temp _pap_camos[0] run data modify storage {ns}:temp _pap_camos set from storage {ns}:zombies camo_variants._default
execute unless data storage {ns}:temp _pap_camos[0] run return 0

data modify storage bs:in random.choice.options set from storage {ns}:temp _pap_camos
function #bs.random:choice
data modify storage {ns}:temp _pap_camo_pick set from storage bs:out random.choice

data modify storage {ns}:temp _pap_camo_data set value {{}}
data modify storage {ns}:temp _pap_camo_data.camo set from storage {ns}:temp _pap_camo_pick

# No scoped weapon id: use the base weapon id.
data modify storage {ns}:temp _pap_camo_data.weapon_id set from storage {ns}:temp _pap_extract.stats.{BASE_WEAPON}
execute if data storage {ns}:temp _pap_extract.weapon run data modify storage {ns}:temp _pap_camo_data.weapon_id set from storage {ns}:temp _pap_extract.weapon
function {ns}:v{version}/zombies/pap/apply_camo with storage {ns}:temp _pap_camo_data
""")

	write_versioned_function("zombies/pap/apply_camo", f"""
# Macro: $(weapon_id) after the scope pick, $(camo) the camo name.
$data modify storage {ns}:temp _pap_extract.stats.models.normal set value "{ns}:$(weapon_id)_$(camo)"
$data modify storage {ns}:temp _pap_extract.stats.models.zoom set value "{ns}:$(weapon_id)_$(camo)_zoom"
""")

	write_versioned_function("zombies/pap/set_item_model_from_scope", """
$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:item_model":"$(model)"}}
""")

	# Like randomize_scope, but never the current scope; _pap_old_weapon must be set.
	write_versioned_function("zombies/pap/randomize_scope_different", f"""
# Nothing to pick with fewer than 2 variants.
$data modify storage {ns}:temp _pap_scopes set from storage {ns}:zombies scope_variants."$({BASE_WEAPON})"
execute unless data storage {ns}:temp _pap_scopes[1] run return 0

function {ns}:v{version}/zombies/pap/randomize_scope with storage {ns}:temp _pap_extract.stats

# `data modify ... set` succeeds only when the value changes.
execute store success score #pap_scope_changed {ns}.data run data modify storage {ns}:temp _pap_old_weapon set from storage {ns}:temp _pap_extract.weapon

# Terminates: there are 2+ variants.
execute if score #pap_scope_changed {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/randomize_scope_different
""")

