
#> mgs:v5.4.2/zombies/save/restore_door_open
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/restore
#			mgs:v5.4.2/zombies/save/restore_door_open
#

execute store result score #sv_id mgs.data run data get storage mgs:temp _sv_iter[0]
scoreboard players set #sv_found mgs.data 0
execute as @e[type=minecraft:interaction,tag=mgs.door] if score @s mgs.zb.door.link = #sv_id mgs.data run scoreboard players set #sv_found mgs.data 1
execute if score #sv_found mgs.data matches 0 run data modify storage mgs:temp _sv_missing append value {element:"doors",id:0}
execute if score #sv_found mgs.data matches 0 store result storage mgs:temp _sv_missing[-1].id int 1 run scoreboard players get #sv_id mgs.data
execute as @e[type=minecraft:interaction,tag=mgs.door] if score @s mgs.zb.door.link = #sv_id mgs.data run scoreboard players set @s mgs.zb.door.anim 1
execute as @e[type=minecraft:interaction,tag=mgs.door] if score @s mgs.zb.door.link = #sv_id mgs.data at @s run function mgs:v5.4.2/zombies/doors/open_one

data remove storage mgs:temp _sv_iter[0]
execute if data storage mgs:temp _sv_iter[0] run function mgs:v5.4.2/zombies/save/restore_door_open

