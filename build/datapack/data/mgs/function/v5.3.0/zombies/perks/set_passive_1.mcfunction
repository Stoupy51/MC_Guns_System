
#> mgs:v5.3.0/zombies/perks/set_passive_1
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/player/config/process
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.passive 1
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.passive_set","fallback":"Passive set: ","color":"gray"},{"translate":"mgs.x1_2_points","fallback":"x1.2 Points","color":"gold"}]
function mgs:v5.3.0/zombies/ability_menu

