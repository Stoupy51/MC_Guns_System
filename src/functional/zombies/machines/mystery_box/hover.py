""" The hover actionbar for each box state. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_mystery_box_hover() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hover functions for active mystery box
	write_versioned_function("zombies/mystery_box/hud_ready", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Click to collect!","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	# Ready + the weapon name is known: prompt the pick-up by name, e.g.
	# "🎲 Pick-up Ray Gun" (_mb_hover_name is the ready display item's item_name, read in hover_at_box)
	write_versioned_function("zombies/mystery_box/hud_ready_named", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎲 ","color":"light_purple"}},{{"text":"Pick-up ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_hover_name","interpret":true}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_spinning", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Spinning...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_price", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎲 Mystery Box","color":"light_purple"}},{{"text":" - ","color":"gray"}},{{"score":{{"name":"#zb_mystery_box_price","objective":"{ns}.config"}},"color":"gold"}},{{"text":" points","color":"gold"}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_moving", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Moving...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/on_hover", f"""
# Only over a usable box (active, any box during a Fire Sale, or a box with a pull in progress)
scoreboard players set #mb_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run scoreboard players set #mb_usable {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mb_fs_active] run scoreboard players set #mb_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_usable {ns}.data 1
execute if score #mb_usable {ns}.data matches 0 run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Active box mid-move
execute if score #mb_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return run function {ns}:v{version}/zombies/mystery_box/hud_moving

# This box's pull state (at the box)
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/hover_at_box
""")

	## Per-box hover state (@s = player, positioned at the box)
	write_versioned_function("zombies/mystery_box/hover_at_box", f"""
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return run function {ns}:v{version}/zombies/mystery_box/hud_spinning
# Ready: name the weapon waiting to be collected (read its item_name; fall back to a generic prompt)
data remove storage {ns}:temp _mb_hover_name
execute if entity @n[tag={ns}.mb_display,distance=..3] run data modify storage {ns}:temp _mb_hover_name set from entity @n[tag={ns}.mb_display,distance=..3] item.components."minecraft:item_name"
execute if entity @n[tag={ns}.mb_display,distance=..3] if data storage {ns}:temp _mb_hover_name run return run function {ns}:v{version}/zombies/mystery_box/hud_ready_named
execute if entity @n[tag={ns}.mb_display,distance=..3] run return run function {ns}:v{version}/zombies/mystery_box/hud_ready
function {ns}:v{version}/zombies/mystery_box/hud_price
""")

