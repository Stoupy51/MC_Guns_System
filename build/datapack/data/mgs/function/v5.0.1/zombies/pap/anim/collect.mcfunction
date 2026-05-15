
#> mgs:v5.0.1/zombies/pap/anim/collect
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.1/zombies/pap/on_right_click
#

# Tag the clicking player so machine-context functions can target them precisely
tag @s add mgs.pap_owner
execute store result score #pap_mid mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
execute if score @s mgs.zb.pap_mid = #pap_mid mgs.data as @n[tag=bs.interaction.target] at @s run function mgs:v5.0.1/zombies/pap/anim/collect_at_machine
execute unless score @s mgs.zb.pap_mid = #pap_mid mgs.data run function mgs:v5.0.1/zombies/pap/anim/deny_not_your_weapon
tag @s remove mgs.pap_owner

