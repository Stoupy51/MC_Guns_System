
#> mgs:v5.0.0/zombies/power/place_at
#
# @within	mgs:v5.0.0/zombies/power/setup_iter with storage mgs:temp _pw
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			facing (unknown)
#

# Place lever block
$setblock $(x) $(y) $(z) minecraft:lever[face=wall,facing=$(facing),powered=false]

# Summon interaction entity with Bookshelf tag and facing tag
$summon minecraft:interaction $(x) $(y) $(z) {width:0.9f,height:0.9f,response:true,Tags:["mgs.power_switch","mgs.gm_entity","bs.entity.interaction","mgs.pw_face_$(facing)","_pw_new"]}

# Register Bookshelf events on newly spawned entity
execute as @e[tag=_pw_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/power/on_activate",executor:"source"}
execute as @e[tag=_pw_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/power/on_hover",executor:"source"}
tag @e[tag=_pw_new] remove _pw_new

