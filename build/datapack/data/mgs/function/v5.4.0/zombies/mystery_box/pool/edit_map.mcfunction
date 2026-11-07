
#> mgs:v5.4.0/zombies/mystery_box/pool/edit_map
#
# @within	mgs:v5.4.0/dialog/close_then
#			dialog mgs:v5.4.0/zombies/setup
#

execute unless data storage mgs:zombies game.map_id run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.select_a_zombies_map_first","fallback":"Select a zombies map first.","color":"red"}]
data modify storage mgs:temp _mb_cur set from storage mgs:config zombies.mystery_box_pool
function mgs:v5.4.0/zombies/mystery_box/pool/map_current with storage mgs:zombies game
function mgs:v5.4.0/zombies/mystery_box/pool/dialog_map

