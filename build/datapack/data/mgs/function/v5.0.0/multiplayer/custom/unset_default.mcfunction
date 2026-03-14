
#> mgs:v5.0.0/multiplayer/custom/unset_default
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Unset default custom loadout - use standard class instead
scoreboard players set @s mgs.mp.default 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.default_loadout_cleared_standard_class_will_be_used","color":"green"}]

