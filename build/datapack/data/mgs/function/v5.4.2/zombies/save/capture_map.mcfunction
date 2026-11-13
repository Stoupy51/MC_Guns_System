
#> mgs:v5.4.2/zombies/save/capture_map
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/save
#

execute store result storage mgs:zombies_saves _slot.map.power byte 1 run scoreboard players get #zb_power mgs.data

# An opened door group has no entity left: a map door whose link id matches none was opened.
data modify storage mgs:temp _sv_doors set from storage mgs:zombies game.map.doors
execute if data storage mgs:temp _sv_doors[0] run function mgs:v5.4.2/zombies/save/capture_door_open

execute store result storage mgs:zombies_saves _slot.map.box_pulls int 1 run scoreboard players get #mb_pulls mgs.data
execute store result storage mgs:zombies_saves _slot.map.box_dry_ray_gun int 1 run scoreboard players get #mb_dry_ray_gun mgs.data
execute as @e[tag=mgs.mystery_box_active,limit=1] store result storage mgs:zombies_saves _slot.map.box int 1 run scoreboard players get @s mgs.mb.box
execute store result storage mgs:zombies_saves _slot.map.wunderfizz_uses int 1 run scoreboard players get #wf_uses mgs.data
execute as @e[tag=mgs.wf_active,limit=1] store result storage mgs:zombies_saves _slot.map.wunderfizz int 1 run scoreboard players get @s mgs.zb.wf.id

execute as @e[type=minecraft:interaction,tag=mgs.door] run function mgs:v5.4.2/zombies/save/capture_doors
execute as @e[type=minecraft:block_display,tag=mgs.barricade_display] run function mgs:v5.4.2/zombies/save/capture_barricades
execute as @e[type=minecraft:marker,tag=mgs.trap_center] run function mgs:v5.4.2/zombies/save/capture_traps
tag @e[tag=mgs.sv_captured] remove mgs.sv_captured

