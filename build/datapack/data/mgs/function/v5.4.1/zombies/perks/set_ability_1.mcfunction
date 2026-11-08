
#> mgs:v5.4.1/zombies/perks/set_ability_1
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/config/process
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.ability 1
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ability_set","fallback":"Ability set: ","color":"gray"},{"translate":"mgs.coward","fallback":"Coward","color":"yellow"},{"translate":"mgs.tp_to_spawn_when_below_50_hp","fallback":" (TP to spawn when below 50% HP)","color":"gray"}]

