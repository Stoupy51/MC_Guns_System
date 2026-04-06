
#> mgs:v5.0.0/zombies/pap/anim/collect
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

# Tag the clicking player so machine-context functions can target them precisely
tag @s add mgs.pap_owner
execute as @n[tag=bs.interaction.target] at @s run function mgs:v5.0.0/zombies/pap/anim/collect_at_machine
tag @s remove mgs.pap_owner

