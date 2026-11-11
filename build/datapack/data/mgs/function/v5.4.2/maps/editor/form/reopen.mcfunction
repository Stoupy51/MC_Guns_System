
#> mgs:v5.4.2/maps/editor/form/reopen
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/form/open_target [ as @n[type=minecraft:marker,tag=mgs.ed_form_target] ]
#			mgs:v5.4.2/maps/editor/form/box_second [ as @n[type=minecraft:marker,tag=mgs.ed_form_target] ]
#

execute if entity @s[tag=mgs.element.zombie_spawn] run function mgs:v5.4.2/maps/editor/form/open/zombie_spawn
execute if entity @s[tag=mgs.element.special_spawn] run function mgs:v5.4.2/maps/editor/form/open/special_spawn
execute if entity @s[tag=mgs.element.mystery_box_pos] run function mgs:v5.4.2/maps/editor/form/open/mystery_box_pos
execute if entity @s[tag=mgs.element.wallbuy] run function mgs:v5.4.2/maps/editor/form/open/wallbuy
execute if entity @s[tag=mgs.element.perk_machine] run function mgs:v5.4.2/maps/editor/form/open/perk_machine
execute if entity @s[tag=mgs.element.trap] run function mgs:v5.4.2/maps/editor/form/open/trap

