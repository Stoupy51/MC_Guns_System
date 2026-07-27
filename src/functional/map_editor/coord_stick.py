""" The coord stick: reading a block's absolute or map-relative position. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_coord_stick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Coord Stick.
	# Detection in player/tick (prepend so it runs before scoreboard reset)
	write_versioned_function("player/tick", f"""
# Coord stick: detect right-click on coord stick
execute if score @s {ns}.class_menu matches 1.. if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{coord_stick:true}}}}] run function {ns}:v{version}/utils/coord_stick
""", prepend=True)

	## Entry point (runs as player)
	write_versioned_function("utils/coord_stick", f"""
# Tag the player so tellraw can target them from inside the at-aimed-block context
tag @s add {ns}.coord_stick_user
function #bs.view:at_aimed_block {{run:"function {ns}:v{version}/utils/coord_stick_relative",with:{{}}}}
tag @s remove {ns}.coord_stick_user
""")

	## State machine — runs at the aimed block
	write_versioned_function("utils/coord_stick_relative", f"""
# State: 0 = first click, 1 = second click (origin already saved)
scoreboard players set #cs_state {ns}.data 0
execute if data storage {ns}:temp coord_stick.origin run scoreboard players set #cs_state {ns}.data 1

# Particle at block center
execute align xyz run particle firework ~.5 ~.5 ~.5 0.4 0.4 0.4 0.01 100 force @a[distance=..20]

# --- Second click: compute relative offset ---
execute if score #cs_state {ns}.data matches 1 summon marker run function {ns}:v{version}/utils/coord_stick_store_pos
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_x {ns}.data = #cs_pos_x {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_y {ns}.data = #cs_pos_y {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_z {ns}.data = #cs_pos_z {ns}.data
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_x {ns}.data run data get storage {ns}:temp coord_stick.origin[0]
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_y {ns}.data run data get storage {ns}:temp coord_stick.origin[1]
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_z {ns}.data run data get storage {ns}:temp coord_stick.origin[2]
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_x {ns}.data -= #cs_orig_x {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_y {ns}.data -= #cs_orig_y {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_z {ns}.data -= #cs_orig_z {ns}.data
execute if score #cs_state {ns}.data matches 1 run data modify storage {ns}:temp coord_stick.result set value {{x:0,y:0,z:0}}
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.x int 1 run scoreboard players get #cs_dest_x {ns}.data
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.y int 1 run scoreboard players get #cs_dest_y {ns}.data
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.z int 1 run scoreboard players get #cs_dest_z {ns}.data
execute if score #cs_state {ns}.data matches 1 as @a[tag={ns}.coord_stick_user,limit=1] run function {ns}:v{version}/utils/coord_stick_print with storage {ns}:temp coord_stick.result
execute if score #cs_state {ns}.data matches 1 run data remove storage {ns}:temp coord_stick.result
execute if score #cs_state {ns}.data matches 1 run data remove storage {ns}:temp coord_stick.origin

# --- First click: record origin position ---
execute if score #cs_state {ns}.data matches 0 summon marker run function {ns}:v{version}/utils/coord_stick_store_pos
execute if score #cs_state {ns}.data matches 0 run data modify storage {ns}:temp coord_stick.origin set value [0,0,0]
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[0] int 1 run scoreboard players get #cs_pos_x {ns}.data
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[1] int 1 run scoreboard players get #cs_pos_y {ns}.data
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[2] int 1 run scoreboard players get #cs_pos_z {ns}.data
execute if score #cs_state {ns}.data matches 0 as @a[tag={ns}.coord_stick_user,limit=1] run tellraw @s [{MGS_TAG},{{"text":"First position saved! Right-click again to get the offset.","color":"yellow"}}]
""")

	## Stores current entity Pos into #cs_pos_x/y/z scores, then kills the marker
	write_versioned_function("utils/coord_stick_store_pos", f"""
execute store result score #cs_pos_x {ns}.data run data get entity @s Pos[0]
execute store result score #cs_pos_y {ns}.data run data get entity @s Pos[1]
execute store result score #cs_pos_z {ns}.data run data get entity @s Pos[2]
kill @s
""")

	## Macro print: outputs "positioned ~X ~Y ~Z" with copy-to-clipboard click event
	write_versioned_function("utils/coord_stick_print", f"""
$tellraw @s [{MGS_TAG},{{"text":"positioned ~$(x) ~$(y) ~$(z)","color":"aqua","click_event":{{"action":"copy_to_clipboard","value":"positioned ~$(x) ~$(y) ~$(z)"}},"hover_event":{{"action":"show_text","value":"Click to copy"}}}}]
""")

