
#> mgs:v5.0.1/zombies/traps/place_turret_at
#
# @within	mgs:v5.0.1/zombies/traps/setup_iter with storage mgs:temp _trap
#
# @args		cx (unknown)
#			cy (unknown)
#			cz (unknown)
#			yaw (unknown)
#

$execute positioned $(cx) $(cy) $(cz) run summon minecraft:item_display ~ ~.5 ~ {Rotation:[$(yaw)f,0f],Tags:["mgs.trap_base","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:iron_block",count:1,components:{"minecraft:item_model":"mgs:turret_base"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2f,2f,2f]}}
$execute positioned $(cx) $(cy) $(cz) positioned ~ ~1.625 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw)f,0f],Tags:["mgs.trap_head","mgs.gm_entity","mgs._trap_new_head"],item_display:"fixed",billboard:"fixed",teleport_duration:5,item:{id:"minecraft:netherite_block",count:1,components:{"minecraft:item_model":"mgs:turret_head"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}

