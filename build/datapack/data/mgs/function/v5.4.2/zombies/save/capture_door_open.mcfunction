
#> mgs:v5.4.2/zombies/save/capture_door_open
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/capture_map
#			mgs:v5.4.2/zombies/save/capture_door_open
#

execute store result score #sv_id mgs.data run data get storage mgs:temp _sv_doors[0].link_id
scoreboard players set #sv_found mgs.data 0
execute as @e[type=minecraft:interaction,tag=mgs.door] if score @s mgs.zb.door.link = #sv_id mgs.data run scoreboard players set #sv_found mgs.data 1
execute if score #sv_found mgs.data matches 0 run data modify storage mgs:zombies_saves _slot.map.opened append from storage mgs:temp _sv_doors[0].link_id

data remove storage mgs:temp _sv_doors[0]
execute store result storage mgs:temp _sv_link.id int 1 run scoreboard players get #sv_id mgs.data
function mgs:v5.4.2/zombies/save/forget_door_link with storage mgs:temp _sv_link
execute if data storage mgs:temp _sv_doors[0] run function mgs:v5.4.2/zombies/save/capture_door_open

