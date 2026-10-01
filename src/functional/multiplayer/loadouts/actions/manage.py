""" Public/private visibility, the default loadout and re-opening one in the editor. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import TRIG_EDIT_BASE, TRIG_SET_DEFAULT_BASE, TRIG_TOGGLE_VIS_BASE
from ....helpers import MGS_TAG


# Functions
def write_loadout_management() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("multiplayer/custom/toggle_visibility", f"""
# The trigger value carries the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_TOGGLE_VIS_BASE}

# Rebuild the list, toggling the matching entry.
data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/toggle_vis_rebuild

tellraw @s ["",{MGS_TAG},{{"text":"Loadout visibility toggled","color":"green"}}]

function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	write_versioned_function("multiplayer/custom/toggle_vis_rebuild", f"""
# Same id and owner.
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _del_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _del_src[0].owner_pid
scoreboard players set #vis_match {ns}.data 0
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #vis_match {ns}.data 1

execute if score #vis_match {ns}.data matches 1 run function {ns}:v{version}/multiplayer/custom/toggle_entry_vis

data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/toggle_vis_rebuild
""")

	write_versioned_function("multiplayer/custom/toggle_entry_vis", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _del_src[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _del_src[0].public set value 0b
execute if score #pub {ns}.data matches 0 run data modify storage {ns}:temp _del_src[0].public set value 1b
""")

	## Applied automatically when a game starts.
	write_versioned_function("multiplayer/custom/set_default", f"""
# The trigger value carries the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SET_DEFAULT_BASE}

scoreboard players operation @s {ns}.mp.default = #loadout_id {ns}.data

tellraw @s ["",{MGS_TAG},{{"text":"Default loadout set! It will auto-apply when a game starts","color":"green"}}]
""")

	write_versioned_function("multiplayer/custom/unset_default", f"""
# Back to the standard class.
scoreboard players set @s {ns}.mp.default 0
tellraw @s [{MGS_TAG},{{"text":"Default loadout cleared. Standard class will be used","color":"green"}}]
""")

	## Reopen the editor hub with an existing loadout; saving overwrites it.
	write_versioned_function("multiplayer/custom/edit", f"""
# The trigger value carries the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_EDIT_BASE}

scoreboard players operation @s {ns}.mp.edit_target = #loadout_id {ns}.data

# Empty state first, then the loadout's saved editor_state if any.
function {ns}:v{version}/multiplayer/editor/init_state
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts
scoreboard players set #edit_found {ns}.data 0
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/edit_load_iter

# Loadouts saved before editor_state cannot be pre-filled.
execute if score #edit_found {ns}.data matches 0 run tellraw @s [{MGS_TAG},{{"text":"This loadout predates editing support. Rebuild it from scratch (saving still overwrites it).","color":"yellow"}}]

# Points are recomputed from the loaded state.
function {ns}:v{version}/multiplayer/editor/hub
""")

	## Find the loadout by id and copy its editor_state.
	write_versioned_function("multiplayer/custom/edit_load_iter", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if data storage {ns}:temp _find_iter[0].editor_state run data modify storage {ns}:temp editor set from storage {ns}:temp _find_iter[0].editor_state
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if data storage {ns}:temp _find_iter[0].editor_state run scoreboard players set #edit_found {ns}.data 1
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return 0

data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/edit_load_iter
""")

