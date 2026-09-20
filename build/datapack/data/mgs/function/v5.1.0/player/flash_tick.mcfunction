
#> mgs:v5.1.0/player/flash_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# @s = a player with a flash applied. Counting down to 0 takes the id off and frees the clock.
scoreboard players remove @s mgs.flash_off 1
execute if score @s mgs.flash_off matches 1.. run return 0
execute if score @s mgs.flash_id matches 1 run posteffect remove @s mgs:flash_zoom
execute if score @s mgs.flash_id matches 2 run posteffect remove @s mgs:flash_pap_zoom
execute if score @s mgs.flash_id matches 3 run posteffect remove @s mgs:flash
execute if score @s mgs.flash_id matches 4 run posteffect remove @s mgs:flash_pap
scoreboard players set @s mgs.flash_id 0
scoreboard players reset @s mgs.flash_off

