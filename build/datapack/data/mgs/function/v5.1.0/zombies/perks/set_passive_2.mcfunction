
#> mgs:v5.1.0/zombies/perks/set_passive_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Zonweeb variant only
execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.passive 2
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.passive_set","color":"gray"},{"translate":"mgs.x1_5_powerups","color":"aqua"}]
function mgs:v5.1.0/zombies/ability_menu

