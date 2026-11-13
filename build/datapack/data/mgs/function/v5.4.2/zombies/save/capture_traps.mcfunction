
#> mgs:v5.4.2/zombies/save/capture_traps
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/capture_map [ as @e[type=minecraft:marker,tag=mgs.trap_center] ]
#

execute if entity @s[tag=mgs.sv_captured] run return 0
scoreboard players operation #sv_id mgs.data = @s mgs.zb.trap.id
execute as @e[type=minecraft:marker,tag=mgs.trap_center] if score @s mgs.zb.trap.id = #sv_id mgs.data run tag @s add mgs.sv_captured

data modify storage mgs:zombies_saves _slot.map.traps append value {}
execute store result storage mgs:zombies_saves _slot.map.traps[-1].id int 1 run scoreboard players get @s mgs.zb.trap.id
execute store result storage mgs:zombies_saves _slot.map.traps[-1].cd int 1 run scoreboard players get @s mgs.zb.trap.cd

