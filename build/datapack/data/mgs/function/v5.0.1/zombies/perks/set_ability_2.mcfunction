
#> mgs:v5.0.1/zombies/perks/set_ability_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Zonweeb variant only
execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.ability 2
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.ability_set","color":"gray"},{"translate":"mgs.guardian","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.summon_an_iron_golem_ally"}]]

