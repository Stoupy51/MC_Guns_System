
#> mgs:v5.3.0/maps/zombies/kino_der_toten/setup_lure
#
# @within	#mgs:zombies/setup_lure
#

execute if data storage mgs:zombies game{map_id:"kino_der_toten"} positioned ~-49 ~-3 ~0 run summon minecraft:marker ~ ~ ~ {CustomName:"Lure Centre",Tags:["mgs.lure_center","mgs.zombies_entity"]}

