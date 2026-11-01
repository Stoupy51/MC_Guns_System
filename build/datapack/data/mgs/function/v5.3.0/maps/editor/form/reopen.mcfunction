
#> mgs:v5.3.0/maps/editor/form/reopen
#
# @executed	as @n[type=minecraft:marker,tag=mgs.ed_form_target]
#
# @within	mgs:v5.3.0/maps/editor/form/open_target [ as @n[type=minecraft:marker,tag=mgs.ed_form_target] ]
#			mgs:v5.3.0/maps/editor/form/box_second [ as @n[type=minecraft:marker,tag=mgs.ed_form_target] ]
#

execute if entity @s[tag=mgs.element.zombie_spawn] run function mgs:v5.3.0/maps/editor/form/open/zombie_spawn
execute if entity @s[tag=mgs.element.special_spawn] run function mgs:v5.3.0/maps/editor/form/open/special_spawn
execute if entity @s[tag=mgs.element.mystery_box_pos] run function mgs:v5.3.0/maps/editor/form/open/mystery_box_pos

