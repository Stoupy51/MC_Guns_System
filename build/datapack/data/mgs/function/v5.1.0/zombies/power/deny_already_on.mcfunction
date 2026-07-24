
#> mgs:v5.1.0/zombies/power/deny_already_on
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.1.0/zombies/power/on_activate
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.power_is_already_on","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

