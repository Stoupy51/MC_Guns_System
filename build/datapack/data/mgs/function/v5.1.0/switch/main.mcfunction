
#> mgs:v5.1.0/switch/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

execute if data storage mgs:gun all.gun unless data storage mgs:gun all.stats.weapon_id run function mgs:v5.1.0/switch/set_weapon_id

# A different weapon than last tick starts the switch cooldown.
scoreboard players set #current_id mgs.data 0
execute store result score #current_id mgs.data run data get storage mgs:gun all.stats.weapon_id
execute unless score @s mgs.last_selected = #current_id mgs.data run function mgs:v5.1.0/switch/on_weapon_switch

scoreboard players operation @s mgs.last_selected = #current_id mgs.data

