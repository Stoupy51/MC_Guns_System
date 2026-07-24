
#> mgs:v5.1.0/zombies/power/on_activate
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.1.0/zombies/power/place_at {run:"function mgs:v5.1.0/zombies/power/on_activate",executor:"source"} [ as @e[tag=_pw_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Guard: power must not already be on
execute if score #zb_power mgs.data matches 1 run return run function mgs:v5.1.0/zombies/power/deny_already_on

# Enable power
scoreboard players set #zb_power mgs.data 1

# Effects at each power switch position
execute as @e[tag=mgs.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=mgs.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Switch every display model to its powered ('on') variant (handle + light go green/lit)
execute as @e[tag=mgs.power_switch_disp] run data modify entity @s item.components."minecraft:item_model" set value "mgs:power_switch_on"

# Kill power switch interaction entities (one-time use); displays stay to show the "on" state
kill @e[tag=mgs.power_switch]

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.power_is_on","color":"green","bold":true}]
playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.9 1.0

# Signal map-specific power-on hooks
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"power"}

