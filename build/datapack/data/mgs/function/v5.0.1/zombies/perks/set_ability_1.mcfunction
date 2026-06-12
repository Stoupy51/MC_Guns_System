
#> mgs:v5.0.1/zombies/perks/set_ability_1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Zonweeb variant only
execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.ability 1
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.ability_set","color":"gray"},{"translate":"mgs.coward","color":"yellow"},{"translate":"mgs.tp_to_spawn_when_below_50_hp","color":"gray"}]

