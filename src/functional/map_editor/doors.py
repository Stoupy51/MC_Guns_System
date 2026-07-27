""" Propagating a field to every door sharing a link id. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_editor_doors() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Door Link Propagation (set selected field on all doors with same link_id)
	write_versioned_function("maps/editor/set_door_link_apply", f"""
execute unless entity @n[tag={ns}.element.door,distance=..10] run return run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No door found within 10 blocks!","color":"red"}}]
execute store result score #link_id {ns}.data run data get entity @n[tag={ns}.element.door,distance=..10] data.link_id
execute as @e[tag={ns}.element.door] run function {ns}:v{version}/maps/editor/door_set_if_match
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Updated ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_door_set.field","color":"yellow"}},{{"text":" for all doors with matching link_id","color":"green"}}]
""")

	write_versioned_function("maps/editor/door_set_if_match", f"""
execute store result score #check {ns}.data run data get entity @s data.link_id
execute if score #check {ns}.data = #link_id {ns}.data run function {ns}:v{version}/maps/editor/door_apply_field with storage {ns}:temp _door_set
""")

	write_versioned_function("maps/editor/door_apply_field", f"""
$data modify entity @s data.$(field) set from storage {ns}:temp _door_set.value
""")

	## Entry points for the door config buttons (macro: field, value)
	write_versioned_function("maps/editor/set_door_link_text", f"""
$data modify storage {ns}:temp _door_set set value {{field:"$(field)",value:"$(value)"}}
function {ns}:v{version}/maps/editor/set_door_link_apply
""")

	write_versioned_function("maps/editor/set_door_link_number", f"""
$data modify storage {ns}:temp _door_set set value {{field:"$(field)",value:$(value)}}
function {ns}:v{version}/maps/editor/set_door_link_apply
""")

