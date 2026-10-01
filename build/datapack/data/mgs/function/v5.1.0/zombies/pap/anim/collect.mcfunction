
#> mgs:v5.1.0/zombies/pap/anim/collect
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/on_right_click
#

# Machine-context functions target the player through this tag.
tag @s add mgs.pap_owner
execute store result score #pap_mid mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id

# Ownership is read into a flag first: collect_give resets zb.pap_mid, so testing it afterwards would trip the deny branch.
scoreboard players set #pap_owns mgs.data 0
execute if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set #pap_owns mgs.data 1

execute if score #pap_owns mgs.data matches 1 as @n[tag=bs.interaction.target] at @s run function mgs:v5.1.0/zombies/pap/anim/collect_at_machine
execute if score #pap_owns mgs.data matches 0 run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.this_upgraded_weapon_belongs_to_another_player","color":"red"}'}
tag @s remove mgs.pap_owner

