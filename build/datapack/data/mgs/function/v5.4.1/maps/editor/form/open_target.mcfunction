
#> mgs:v5.4.1/maps/editor/form/open_target
#
# @within	mgs:v5.4.1/dialog/close_then
#			string in mgs:v5.4.1/maps/editor/show_element_config
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail
execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_element_being_edited_is_gone","fallback":"The element being edited is gone.","color":"red"}]
tag @s add mgs.ed_form_user
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run function mgs:v5.4.1/maps/editor/form/reopen
tag @s remove mgs.ed_form_user

