
#> mgs:v5.4.2/zombies/save/capture_doors
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/capture_map [ as @e[type=minecraft:interaction,tag=mgs.door] ]
#

execute if entity @s[tag=mgs.sv_captured] run return 0
scoreboard players operation #sv_id mgs.data = @s mgs.zb.door.link
execute as @e[type=minecraft:interaction,tag=mgs.door] if score @s mgs.zb.door.link = #sv_id mgs.data run tag @s add mgs.sv_captured

data modify storage mgs:zombies_saves _slot.map.doors append value {}
execute store result storage mgs:zombies_saves _slot.map.doors[-1].id int 1 run scoreboard players get @s mgs.zb.door.link
execute store result storage mgs:zombies_saves _slot.map.doors[-1].paid int 1 run scoreboard players get @s mgs.zb.door.paid

