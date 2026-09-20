
#> mgs:v5.1.0/player/hurt_resolve
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

# @s = an in-game, non-spectating player. `attribute get <scale>` truncates, so a scale of 0.4
# yields the health at which 40% is crossed, keeping the whole check on scores with no NBT read.
execute store result score #hurt_at mgs.data run attribute @s minecraft:max_health get 0.4
execute if score @s mgs.health <= #hurt_at mgs.data run scoreboard players set #hurt_tier mgs.data 1
execute store result score #hurt_at mgs.data run attribute @s minecraft:max_health get 0.2
execute if score @s mgs.health <= #hurt_at mgs.data run scoreboard players set #hurt_tier mgs.data 2

