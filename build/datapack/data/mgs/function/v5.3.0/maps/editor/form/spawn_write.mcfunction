
#> mgs:v5.3.0/maps/editor/form/spawn_write
#
# @executed	as @n[type=minecraft:marker,tag=mgs.ed_form_target]
#
# @within	mgs:v5.3.0/maps/editor/form/spawn_apply [ as @n[type=minecraft:marker,tag=mgs.ed_form_target] ]
#

data modify entity @s data merge from storage mgs:temp _form.data
execute if entity @s[tag=mgs.element.zombie_spawn] run data modify entity @s data.power set from storage mgs:temp _form.power

# An empty mob field puts back the kind's own.
execute if data storage mgs:temp _form.mob[0] run data modify entity @s data.mob set from storage mgs:temp _form.mob[0]
execute unless data storage mgs:temp _form.mob[0] if entity @s[tag=mgs.element.zombie_spawn] run data modify entity @s data.mob set value {entity:"zombie"}
execute unless data storage mgs:temp _form.mob[0] if entity @s[tag=mgs.element.special_spawn] run data modify entity @s data.mob set value {entity:"wolf"}

