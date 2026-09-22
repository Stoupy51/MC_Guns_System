
#> mgs:v5.1.0/player/hurt_swap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

# Start from the look the current id ends on. A hit landing mid-fade starts from the look that fade
# was leaving instead, since that is still close to what is on screen.
scoreboard players operation #hurt_start mgs.data = @s mgs.hurt_fx
execute if score #hurt_tier mgs.data > @s mgs.hurt_fx if score @s mgs.hurt_fall_until > #total_tick mgs.data run scoreboard players operation #hurt_start mgs.data = @s mgs.hurt_from

# The new pair always differs from the old one (its end level changed), so this is never the same id twice
execute if score @s mgs.hurt_from matches 0 if score @s mgs.hurt_fx matches 1 run posteffect remove @s mgs:hurt_0_1
execute if score @s mgs.hurt_from matches 0 if score @s mgs.hurt_fx matches 2 run posteffect remove @s mgs:hurt_0_2
execute if score @s mgs.hurt_from matches 1 if score @s mgs.hurt_fx matches 0 run posteffect remove @s mgs:hurt_1_0
execute if score @s mgs.hurt_from matches 1 if score @s mgs.hurt_fx matches 1 run posteffect remove @s mgs:hurt_1_1
execute if score @s mgs.hurt_from matches 1 if score @s mgs.hurt_fx matches 2 run posteffect remove @s mgs:hurt_1_2
execute if score @s mgs.hurt_from matches 2 if score @s mgs.hurt_fx matches 0 run posteffect remove @s mgs:hurt_2_0
execute if score @s mgs.hurt_from matches 2 if score @s mgs.hurt_fx matches 1 run posteffect remove @s mgs:hurt_2_1
execute if score @s mgs.hurt_from matches 2 if score @s mgs.hurt_fx matches 2 run posteffect remove @s mgs:hurt_2_2
execute if score #hurt_start mgs.data matches 0 if score #hurt_tier mgs.data matches 1 run posteffect add @s mgs:hurt_0_1
execute if score #hurt_start mgs.data matches 0 if score #hurt_tier mgs.data matches 2 run posteffect add @s mgs:hurt_0_2
execute if score #hurt_start mgs.data matches 1 if score #hurt_tier mgs.data matches 0 run posteffect add @s mgs:hurt_1_0
execute if score #hurt_start mgs.data matches 1 if score #hurt_tier mgs.data matches 1 run posteffect add @s mgs:hurt_1_1
execute if score #hurt_start mgs.data matches 1 if score #hurt_tier mgs.data matches 2 run posteffect add @s mgs:hurt_1_2
execute if score #hurt_start mgs.data matches 2 if score #hurt_tier mgs.data matches 0 run posteffect add @s mgs:hurt_2_0
execute if score #hurt_start mgs.data matches 2 if score #hurt_tier mgs.data matches 1 run posteffect add @s mgs:hurt_2_1
execute if score #hurt_start mgs.data matches 2 if score #hurt_tier mgs.data matches 2 run posteffect add @s mgs:hurt_2_2
scoreboard players operation @s mgs.hurt_from = #hurt_start mgs.data
scoreboard players operation @s mgs.hurt_fx = #hurt_tier mgs.data
scoreboard players reset @s mgs.hurt_pending
scoreboard players reset @s mgs.hurt_fall_until
scoreboard players reset @s mgs.hurt_out_until
execute if score #hurt_tier mgs.data < #hurt_start mgs.data run function mgs:v5.1.0/player/hurt_schedule_fall

