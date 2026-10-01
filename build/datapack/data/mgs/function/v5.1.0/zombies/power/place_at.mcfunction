
#> mgs:v5.1.0/zombies/power/place_at
#
# @within	mgs:v5.1.0/zombies/power/setup_iter with storage mgs:temp _pw
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			yaw (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:0.9f,height:0.9f,response:true,Tags:["mgs.power_switch","mgs.gm_entity","bs.entity.interaction","_pw_new"]}

$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw)f,0f],Tags:["mgs.power_switch_disp","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:lever",count:1,components:{"minecraft:item_model":"mgs:power_switch"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}

execute as @e[tag=_pw_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/power/on_activate",executor:"source"}
execute as @e[tag=_pw_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/power/on_hover",executor:"source"}
tag @e[tag=_pw_new] remove _pw_new

