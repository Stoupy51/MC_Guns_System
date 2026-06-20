
#> mgs:v5.0.1/zombies/pap/anim/collect
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.1/zombies/pap/on_right_click
#

# Tag the clicking player so machine-context functions can target them precisely
tag @s add mgs.pap_owner
execute store result score #pap_mid mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id

# Resolve ownership into a flag BEFORE acting: a successful collect (collect_give) resets the
# player's zb.pap_mid to 0, so re-testing the comparison afterwards would spuriously trip the
# deny branch ("belongs to another player") right after the weapon was returned.
scoreboard players set #pap_owns mgs.data 0
execute if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set #pap_owns mgs.data 1

execute if score #pap_owns mgs.data matches 1 as @n[tag=bs.interaction.target] at @s run function mgs:v5.0.1/zombies/pap/anim/collect_at_machine
execute if score #pap_owns mgs.data matches 0 run function mgs:v5.0.1/zombies/pap/anim/deny_not_your_weapon
tag @s remove mgs.pap_owner

