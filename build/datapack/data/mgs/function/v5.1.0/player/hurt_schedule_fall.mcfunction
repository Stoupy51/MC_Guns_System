
#> mgs:v5.1.0/player/hurt_schedule_fall
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_swap
#

scoreboard players set @s mgs.hurt_fall_until 40
scoreboard players operation @s mgs.hurt_fall_until += #total_tick mgs.data

# Fading to nothing: once the fade has played, the id comes off entirely
execute if score #hurt_tier mgs.data matches 0 run scoreboard players operation @s mgs.hurt_out_until = @s mgs.hurt_fall_until
execute if score #hurt_tier mgs.data matches 0 run scoreboard players add @s mgs.hurt_out_until 1

