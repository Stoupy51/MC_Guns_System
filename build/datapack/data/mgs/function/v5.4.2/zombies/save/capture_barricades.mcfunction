
#> mgs:v5.4.2/zombies/save/capture_barricades
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/capture_map [ as @e[type=minecraft:block_display,tag=mgs.barricade_display] ]
#

execute if entity @s[tag=mgs.sv_captured] run return 0
scoreboard players operation #sv_id mgs.data = @s mgs.zb.barricade.id
execute as @e[type=minecraft:block_display,tag=mgs.barricade_display] if score @s mgs.zb.barricade.id = #sv_id mgs.data run tag @s add mgs.sv_captured

data modify storage mgs:zombies_saves _slot.map.barricades append value {}
execute store result storage mgs:zombies_saves _slot.map.barricades[-1].id int 1 run scoreboard players get @s mgs.zb.barricade.id
execute store result storage mgs:zombies_saves _slot.map.barricades[-1].state int 1 run scoreboard players get @s mgs.zb.barricade.state

