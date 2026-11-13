
#> mgs:v5.4.2/zombies/power/on_activate
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/power/place_at {run:"function mgs:v5.4.2/zombies/power/on_activate",executor:"source"} [ as @e[tag=_pw_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

execute if score #zb_power mgs.data matches 1 run return run function mgs:v5.4.2/zombies/deny/message {msg:'{"translate":"mgs.power_is_already_on","fallback":"Power is already on.","color":"yellow"}'}

execute as @e[tag=mgs.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=mgs.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 2 1

function mgs:v5.4.2/zombies/power/turn_on

# The whole roster earns it, so no earner split.
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.power_is_on","fallback":"Power is ON!","color":"green","bold":true},[" ",{"text":"+10 XP","color":"gold"}]]
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.4.2/progression/zb/award_power
playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.9 1.0

