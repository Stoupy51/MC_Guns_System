
#> mgs:v5.3.0/maps/editor/form/mystery_box_apply
#
# @within	string in mgs:v5.3.0/maps/editor/form/open/mystery_box_pos {yaw:$(yaw),pitch:$(pitch),roll:$(roll),can_start_on:$(can_start_on),location_name:\"$(location_name)\"}
#
# @args		yaw (unknown)
#			pitch (unknown)
#			roll (unknown)
#			can_start_on (unknown)
#			location_name (string)
#

execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_element_being_edited_is_gone","fallback":"The element being edited is gone.","color":"red"}]
$data modify storage mgs:temp _form set value {yaw:$(yaw)f,pitch:$(pitch)f,roll:$(roll),can_start_on:$(can_start_on)b,location_name:"$(location_name)"}
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run data modify entity @s data merge from storage mgs:temp _form
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.mystery_box_spot_saved","fallback":"Mystery box spot saved.","color":"green"}]

