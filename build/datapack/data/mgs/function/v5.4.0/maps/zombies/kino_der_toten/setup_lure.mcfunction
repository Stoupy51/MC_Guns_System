
#> mgs:v5.4.0/maps/zombies/kino_der_toten/setup_lure
#
# @within	#mgs:zombies/setup_lure
#			mgs:v5.4.0/dialog/close_then
#

execute if data storage mgs:zombies game{map_id:"kino_der_toten"} positioned ~-49 ~-3 ~0 run summon minecraft:marker ~ ~ ~ {Tags:["mgs.lure_center","mgs.zombies_entity"]}

