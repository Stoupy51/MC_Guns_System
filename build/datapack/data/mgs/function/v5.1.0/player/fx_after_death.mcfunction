
#> mgs:v5.1.0/player/fx_after_death
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players reset @s mgs.flash_id
scoreboard players reset @s mgs.flash_slot
scoreboard players reset @s mgs.flash_off
scoreboard players reset @s mgs.zoom_fx
scoreboard players reset @s mgs.zoom_fx_off
scoreboard players reset @s mgs.cross_from
scoreboard players reset @s mgs.cross_to
scoreboard players reset @s mgs.hurt_fx
scoreboard players reset @s mgs.hurt_from
scoreboard players reset @s mgs.hurt_pending
scoreboard players reset @s mgs.hurt_fall_until
scoreboard players reset @s mgs.hurt_out_until
scoreboard players set @s mgs.fx_deaths 0

