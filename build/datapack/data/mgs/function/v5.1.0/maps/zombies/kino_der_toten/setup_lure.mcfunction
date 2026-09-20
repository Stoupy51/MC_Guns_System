
#> mgs:v5.1.0/maps/zombies/kino_der_toten/setup_lure
#
# @within	#mgs:zombies/setup_lure
#

execute if data storage mgs:zombies game{map_id:"kino_der_toten"} positioned ~-49 ~-3 ~0 run summon minecraft:marker ~ ~ ~ {Tags:["mgs.lure_center","mgs.gm_entity"]}

