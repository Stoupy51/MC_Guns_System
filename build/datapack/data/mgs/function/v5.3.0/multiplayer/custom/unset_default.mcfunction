
#> mgs:v5.3.0/multiplayer/custom/unset_default
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#

# Back to the standard class.
scoreboard players set @s mgs.mp.default 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.default_loadout_cleared_standard_class_will_be_used","fallback":"Default loadout cleared. Standard class will be used","color":"green"}]

