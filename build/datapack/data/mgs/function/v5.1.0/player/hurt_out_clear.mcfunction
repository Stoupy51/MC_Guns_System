
#> mgs:v5.1.0/player/hurt_out_clear
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# @s = a player whose fade to nothing has finished playing
execute if score @s mgs.hurt_from matches 1 if score @s mgs.hurt_fx matches 0 run posteffect remove @s mgs:hurt_1_0
execute if score @s mgs.hurt_from matches 2 if score @s mgs.hurt_fx matches 0 run posteffect remove @s mgs:hurt_2_0
scoreboard players set @s mgs.hurt_from 0
scoreboard players reset @s mgs.hurt_fall_until
scoreboard players reset @s mgs.hurt_out_until

