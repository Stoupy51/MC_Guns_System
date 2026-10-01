
#> mgs:v5.1.0/player/fx_reset
#
# @executed	as @a
#
# @within	mgs:v5.1.0/load/confirm_load [ as @a ]
#			mgs:v5.1.0/player/fx_after_death
#			mgs:v5.1.0/player/fx_after_rejoin
#			mgs:v5.1.0/zombies/start [ as @a ]
#			mgs:v5.1.0/zombies/stop [ as @a ]
#			mgs:v5.1.0/multiplayer/start [ as @a ]
#			mgs:v5.1.0/multiplayer/stop [ as @a ]
#			mgs:v5.1.0/missions/start [ as @a ]
#			mgs:v5.1.0/missions/stop [ as @a ]
#

scoreboard players set #hurt_was mgs.data 0
execute if score @s mgs.hurt_fx matches 1.. run scoreboard players operation #hurt_was mgs.data = @s mgs.hurt_fx
posteffect clear @s
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

# The red overlay fades out instead of vanishing
execute if score #hurt_was mgs.data matches 1.. run function mgs:v5.1.0/player/hurt_fade_out

