
#> mgs:v5.3.0/maps/editor/form/spawn_apply
#
# @within	string in mgs:v5.3.0/maps/editor/form/open/zombie_spawn {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:$(power),mob:\"$(mob)\",activation_box:\"$(activation_box)\",walk_to:\"$(walk_to)\",then:\"\"}
#			string in mgs:v5.3.0/maps/editor/form/open/zombie_spawn {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:$(power),mob:\"$(mob)\",activation_box:\"$(activation_box)\",walk_to:\"$(walk_to)\",then:\"box\"}
#			string in mgs:v5.3.0/maps/editor/form/open/special_spawn {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:0,mob:\"$(mob)\",activation_box:\"$(activation_box)\",walk_to:\"$(walk_to)\",then:\"\"}
#			string in mgs:v5.3.0/maps/editor/form/open/special_spawn {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:0,mob:\"$(mob)\",activation_box:\"$(activation_box)\",walk_to:\"$(walk_to)\",then:\"box\"}
#
# @args		group_id (unknown)
#			min_round (unknown)
#			max_round (unknown)
#			arrival (string)
#			rise_ticks (unknown)
#			activation_box (string)
#			walk_to (string)
#			power (int)
#			mob (string)
#			then (string)
#

$data modify storage mgs:temp _form set value {data:{group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:"$(arrival)",rise_ticks:$(rise_ticks),activation_box:[$(activation_box)],walk_to:[$(walk_to)]},power:$(power)b,mob:[$(mob)],then:"$(then)"}
execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_element_being_edited_is_gone","fallback":"The element being edited is gone.","color":"red"}]
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run function mgs:v5.3.0/maps/editor/form/spawn_write
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.spawn_saved","fallback":"Spawn saved.","color":"green"}]
execute if data storage mgs:temp _form{then:"box"} run function mgs:v5.3.0/maps/editor/form/box_start

