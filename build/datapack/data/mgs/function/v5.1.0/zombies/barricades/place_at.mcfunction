
#> mgs:v5.1.0/zombies/barricades/place_at
#
# @within	mgs:v5.1.0/zombies/barricades/setup_iter with storage mgs:temp _bplace
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			yaw (unknown)
#

$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:block_display ~ ~ ~ {Rotation:[$(yaw)f,0f],block_state:{Name:"minecraft:air"},transformation:{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]},Tags:["mgs.barricade_display","mgs.gm_entity","mgs._barricade_new_d"]}

