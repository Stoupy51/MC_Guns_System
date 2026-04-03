
#> mgs:v5.0.0/zombies/power/on_activate
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.0.0/zombies/power/place_at {run:"function mgs:v5.0.0/zombies/power/on_activate",executor:"source"} [ as @e[tag=_pw_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Guard: power must not already be on
execute if score #zb_power mgs.data matches 1 run return run function mgs:v5.0.0/zombies/power/deny_already_on

# Enable power
scoreboard players set #zb_power mgs.data 1

# Effects at each power switch position
execute as @e[tag=mgs.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=mgs.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Toggle lever blocks to powered state
execute as @e[tag=mgs.power_switch] at @s if entity @s[tag=mgs.pw_face_north] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=north,powered=true]
execute as @e[tag=mgs.power_switch] at @s if entity @s[tag=mgs.pw_face_south] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=south,powered=true]
execute as @e[tag=mgs.power_switch] at @s if entity @s[tag=mgs.pw_face_east] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=east,powered=true]
execute as @e[tag=mgs.power_switch] at @s if entity @s[tag=mgs.pw_face_west] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=west,powered=true]

# Kill power switch interaction entities (one-time use)
kill @e[tag=mgs.power_switch]

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.power_is_on","color":"green","bold":true}]
function mgs:v5.0.0/zombies/feedback/sound_power_on

