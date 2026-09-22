
#> mgs:v5.1.0/player/hurt_fall
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

# Healing: the tier being left hands over to its fade-out twin, while any lower tier still owed ramps in
function mgs:v5.1.0/player/hurt_out_clear
execute if score @s mgs.hurt_fx matches 1 run posteffect remove @s mgs:hurt
execute if score @s mgs.hurt_fx matches 2 run posteffect remove @s mgs:hurt_critical
execute if score @s mgs.hurt_fx matches 1 run posteffect add @s mgs:hurt_out
execute if score @s mgs.hurt_fx matches 2 run posteffect add @s mgs:hurt_critical_out
scoreboard players operation @s mgs.hurt_out = @s mgs.hurt_fx
scoreboard players set @s mgs.hurt_out_until 41
scoreboard players operation @s mgs.hurt_out_until += #total_tick mgs.data
execute if score #hurt_tier mgs.data matches 1 run posteffect add @s mgs:hurt
execute if score #hurt_tier mgs.data matches 2 run posteffect add @s mgs:hurt_critical

