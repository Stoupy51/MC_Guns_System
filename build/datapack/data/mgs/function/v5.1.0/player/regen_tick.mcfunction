
#> mgs:v5.1.0/player/regen_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# @s = any player during an active game
# Damage detection via the auto-updated 'health' criterion (no player-NBT read)
execute if score @s mgs.health < @s mgs.hp_prev run scoreboard players set @s mgs.last_hit 0
execute unless score @s mgs.health < @s mgs.hp_prev run scoreboard players add @s mgs.last_hit 1
scoreboard players operation @s mgs.hp_prev = @s mgs.health
execute unless score @s mgs.last_hit matches 100.. run return 0

# At full health there is nothing to refresh; a still-running 3s pulse finishes any half-heart
# (regeneration can't overheal, so letting it expire replaces the old per-tick `effect clear`)
execute store result score #hp_max mgs.data run attribute @s minecraft:max_health get 1
execute if score @s mgs.health >= #hp_max mgs.data run return 0
effect give @s minecraft:regeneration 3 2 true

