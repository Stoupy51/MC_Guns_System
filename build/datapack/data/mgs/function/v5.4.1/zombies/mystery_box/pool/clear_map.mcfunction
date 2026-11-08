
#> mgs:v5.4.1/zombies/mystery_box/pool/clear_map
#
# @within	mgs:v5.4.1/dialog/close_then
#			dialog mgs:v5.4.1/zombies/setup
#

execute unless data storage mgs:zombies game.map_id run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.select_a_zombies_map_first","fallback":"Select a zombies map first.","color":"red"}]
function mgs:v5.4.1/zombies/mystery_box/pool/remove_map with storage mgs:zombies game

