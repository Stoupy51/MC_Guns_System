""" Selecting a custom loadout and deleting one you own. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import TRIG_DELETE_BASE, TRIG_SELECT_BASE
from ....helpers import MGS_TAG


# Functions
def write_loadout_selection() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Custom loadout actions: select, delete, toggle visibility, set default.

	## Stored now, applied on respawn or apply_class.
	write_versioned_function("multiplayer/custom/select", f"""
# id = trigger - {TRIG_SELECT_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SELECT_BASE}

# A custom loadout is a negative mp.class.
scoreboard players operation @s {ns}.mp.class = #loadout_id {ns}.data
scoreboard players operation @s {ns}.mp.class *= #minus_one {ns}.data

# For the notification.
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_notify
""")

	write_versioned_function("multiplayer/custom/find_and_notify", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return run function {ns}:v{version}/multiplayer/custom/notify_selected with storage {ns}:temp _find_iter[0]

data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_notify
""")

	## Same message as set_class, with the operator apply button.
	apply_now: str = f"""{{"text":" [✔]","color":"gold","hover_event":{{"action":"show_text","value":{{"text":"Click here to apply immediately (OP only)","color":"yellow"}}}},"click_event":{{"action":"suggest_command","command":"/function {ns}:v{version}/multiplayer/apply_class"}}}}"""
	write_versioned_function("multiplayer/custom/notify_selected", f"""$tellraw @s ["",{MGS_TAG},["",{{"text":"Class set to"}}," "],{{"text":"$(name)","color":"green","bold":true}},[{{"text":"","color":"aqua"}}," (",{{"text":"custom"}},")"],{{"text":" - will apply on respawn","color":"yellow"}},{apply_now}]
""")

	## Only the owner can delete.
	write_versioned_function("multiplayer/custom/delete", f"""
# id = trigger - {TRIG_DELETE_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_DELETE_BASE}

data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []

# Skips the entry matching both id and owner.
scoreboard players set #del_removed {ns}.data 0
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter

# Reset the default and active class if they pointed at it.
scoreboard players operation #del_neg_id {ns}.data = #loadout_id {ns}.data
scoreboard players operation #del_neg_id {ns}.data *= #minus_one {ns}.data
execute if score #del_removed {ns}.data matches 1 if score @s {ns}.mp.default = #loadout_id {ns}.data run scoreboard players set @s {ns}.mp.default 0
execute if score #del_removed {ns}.data matches 1 if score @s {ns}.mp.class = #del_neg_id {ns}.data run scoreboard players set @s {ns}.mp.class 0

tellraw @s ["",{MGS_TAG},{{"text":"Loadout deleted","color":"red"}}]

function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	write_versioned_function("multiplayer/custom/delete_filter", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _del_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _del_src[0].owner_pid
scoreboard players set #del_match {ns}.data 0
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #del_match {ns}.data 1
execute if score #del_match {ns}.data matches 1 run scoreboard players set #del_removed {ns}.data 1

execute unless score #del_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter
""")

