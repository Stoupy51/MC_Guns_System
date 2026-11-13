
#> mgs:v5.4.2/zombies/power/turn_on
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/power/on_activate
#			mgs:v5.4.2/zombies/save/restore
#

scoreboard players set #zb_power mgs.data 1
tag @e[type=minecraft:marker,tag=mgs.spawn_point] add mgs.spawn_powered

# Displays switch to the lit model.
execute as @e[tag=mgs.power_switch_disp] run data modify entity @s item.components."minecraft:item_model" set value "mgs:power_switch_on"

# One-time use: the interactions go, the displays stay.
kill @e[tag=mgs.power_switch]

function mgs:v5.4.2/shared/maps/call_script_at_base {mode:"zombies",script:"power"}

