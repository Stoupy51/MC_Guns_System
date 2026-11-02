
#> mgs:v5.3.0/maps/compact/door_link
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.3.0/maps/editor/save_zb_object
#			mgs:v5.3.0/maps/compact/door_block with storage mgs:temp _save_zb
#
# @args		link_id (unknown)
#

$execute unless data storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}] run function mgs:v5.3.0/maps/compact/door_new
$data modify storage mgs:temp _door_link set from storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}]

data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.block
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.block
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.block set from storage mgs:temp _save_zb.block
execute store result score #link_yaw mgs.data run data get storage mgs:temp _door_link.yaw
execute unless score #yaw mgs.data = #link_yaw mgs.data store result storage mgs:temp _door_block.yaw int 1 run scoreboard players get #yaw mgs.data
$data modify storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}].blocks append from storage mgs:temp _door_block

data remove storage mgs:temp _door_link.blocks
data remove storage mgs:temp _door_link.block
data remove storage mgs:temp _door_link.yaw
data remove storage mgs:temp _save_zb.block
data remove storage mgs:temp _save_zb.yaw
execute store success score #differs mgs.data run data modify storage mgs:temp _door_link set from storage mgs:temp _save_zb
execute if score #differs mgs.data matches 1 run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],[{"text":"⚠ ","color":"yellow"}, {"translate":"mgs.the_door_at","fallback":"The door at "}],{"entity":"@s","nbt":"Pos","color":"white"},{"translate":"mgs.differs_from_the_rest_of_link","fallback":" differs from the rest of link ","color":"yellow"},{"storage":"mgs:temp","nbt":"_save_zb.link_id","color":"white"},{"translate":"mgs.which_keeps_the_values_of_one_of_its_doors_the_buttons_of_a_door","fallback":", which keeps the values of one of its doors. The ✎ buttons of a door set its whole link.","color":"yellow"}]

