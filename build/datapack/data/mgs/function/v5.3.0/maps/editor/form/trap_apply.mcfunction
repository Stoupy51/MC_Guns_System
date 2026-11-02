
#> mgs:v5.3.0/maps/editor/form/trap_apply
#
# @within	string in mgs:v5.3.0/maps/editor/form/open/trap {type:$(type),price:$(price),duration:$(duration),cooldown:$(cooldown),power:$(power),effect_radius:\"$(effect_radius)\",offset_pos:\"$(offset_pos)\"}
#
# @args		type (unknown)
#			price (unknown)
#			duration (unknown)
#			cooldown (unknown)
#			power (unknown)
#			effect_radius (string)
#			offset_pos (string)
#

execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_element_being_edited_is_gone","fallback":"The element being edited is gone.","color":"red"}]
$data modify storage mgs:temp _form set value {type:$(type),price:$(price),duration:$(duration),cooldown:$(cooldown),power:$(power)b,effect_radius:[$(effect_radius)],offset_pos:[$(offset_pos)]}
execute store result storage mgs:temp _form.effect_radius[0] float 0.01 run data get storage mgs:temp _form.effect_radius[0] 100
execute store result storage mgs:temp _form.effect_radius[1] float 0.01 run data get storage mgs:temp _form.effect_radius[1] 100
execute store result storage mgs:temp _form.effect_radius[2] float 0.01 run data get storage mgs:temp _form.effect_radius[2] 100
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run data modify entity @s data merge from storage mgs:temp _form
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.trap_saved","fallback":"Trap saved.","color":"green"}]

