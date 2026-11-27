
#> mgs:v5.4.4/maps/compact/door_link
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/maps/editor/save_zb_object
#			mgs:v5.4.4/maps/compact/door_block with storage mgs:temp _save_zb
#
# @args		link_id (unknown)
#

$execute unless data storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}] run function mgs:v5.4.4/maps/compact/door_new
$data modify storage mgs:temp _door_link set from storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}]

execute unless data storage mgs:temp _save_zb.name run data modify storage mgs:temp _save_zb.name set value "Door"
execute unless data storage mgs:temp _door_link.name run data modify storage mgs:temp _door_link.name set value "Door"
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.name
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.name
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.name set from storage mgs:temp _save_zb.name
execute unless data storage mgs:temp _save_zb.back_name run data modify storage mgs:temp _save_zb.back_name set value "Door"
execute unless data storage mgs:temp _door_link.back_name run data modify storage mgs:temp _door_link.back_name set value "Door"
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.back_name
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.back_name
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.back_name set from storage mgs:temp _save_zb.back_name
execute unless data storage mgs:temp _save_zb.price run data modify storage mgs:temp _save_zb.price set value 1000
execute unless data storage mgs:temp _door_link.price run data modify storage mgs:temp _door_link.price set value 1000
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.price
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.price
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.price set from storage mgs:temp _save_zb.price
execute unless data storage mgs:temp _save_zb.partial_price run data modify storage mgs:temp _save_zb.partial_price set value 0
execute unless data storage mgs:temp _door_link.partial_price run data modify storage mgs:temp _door_link.partial_price set value 0
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.partial_price
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.partial_price
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.partial_price set from storage mgs:temp _save_zb.partial_price
execute unless data storage mgs:temp _save_zb.back_group_id run data modify storage mgs:temp _save_zb.back_group_id set value -1
execute unless data storage mgs:temp _door_link.back_group_id run data modify storage mgs:temp _door_link.back_group_id set value -1
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.back_group_id
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.back_group_id
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.back_group_id set from storage mgs:temp _save_zb.back_group_id
execute unless data storage mgs:temp _save_zb.min_round run data modify storage mgs:temp _save_zb.min_round set value 0
execute unless data storage mgs:temp _door_link.min_round run data modify storage mgs:temp _door_link.min_round set value 0
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.min_round
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.min_round
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.min_round set from storage mgs:temp _save_zb.min_round
execute unless data storage mgs:temp _save_zb.block run data modify storage mgs:temp _save_zb.block set value ""
execute unless data storage mgs:temp _door_link.block run data modify storage mgs:temp _door_link.block set value ""
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.block
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.block
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.block set from storage mgs:temp _save_zb.block
execute unless data storage mgs:temp _save_zb.animation run data modify storage mgs:temp _save_zb.animation set value 0
execute unless data storage mgs:temp _door_link.animation run data modify storage mgs:temp _door_link.animation set value 0
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.animation
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.animation
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.animation set from storage mgs:temp _save_zb.animation
execute unless data storage mgs:temp _save_zb.sound run data modify storage mgs:temp _save_zb.sound set value ""
execute unless data storage mgs:temp _door_link.sound run data modify storage mgs:temp _door_link.sound set value ""
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.sound
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp _door_link.sound
execute if score #differs mgs.data matches 1 run data modify storage mgs:temp _door_block.sound set from storage mgs:temp _save_zb.sound
execute store result score #link_yaw mgs.data run data get storage mgs:temp _door_link.yaw
execute unless score #yaw mgs.data = #link_yaw mgs.data store result storage mgs:temp _door_block.yaw int 1 run scoreboard players get #yaw mgs.data
$data modify storage mgs:temp map_edit.map.doors[{link_id:$(link_id)}].blocks append from storage mgs:temp _door_block

