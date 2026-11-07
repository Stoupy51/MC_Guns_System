
#> mgs:v5.4.0/zombies/admin/freeze_toggle
#
# @within	mgs:v5.4.0/dialog/close_then
#			dialog mgs:v5.4.0/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_zombies_game_is_active","fallback":"No zombies game is active.","color":"red"}]
execute if score #zb_freeze mgs.data matches 1.. run return run function mgs:v5.4.0/zombies/freeze_off
function mgs:v5.4.0/zombies/freeze_on

