
#> mgs:v5.1.0/zombies/power/on_activate
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.1.0/zombies/power/place_at {run:"function mgs:v5.1.0/zombies/power/on_activate",executor:"source"} [ as @e[tag=_pw_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

execute if score #zb_power mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.power_is_already_on","color":"yellow"}'}

scoreboard players set #zb_power mgs.data 1

execute as @e[tag=mgs.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=mgs.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Displays switch to the lit model.
execute as @e[tag=mgs.power_switch_disp] run data modify entity @s item.components."minecraft:item_model" set value "mgs:power_switch_on"

# One-time use: the interactions go, the displays stay.
kill @e[tag=mgs.power_switch]

# The whole roster earns it, so no earner split.
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.power_is_on","color":"green","bold":true},[" ",{"text":"+10 XP","color":"gold"}]]
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/progression/zb/award_power
playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.9 1.0

function mgs:v5.1.0/shared/maps/call_script_at_base {script:"power"}

