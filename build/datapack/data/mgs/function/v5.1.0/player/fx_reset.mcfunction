
#> mgs:v5.1.0/player/fx_reset
#
# @executed	as @a
#
# @within	mgs:v5.1.0/zombies/start [ as @a ]
#			mgs:v5.1.0/zombies/stop [ as @a ]
#			mgs:v5.1.0/multiplayer/start [ as @a ]
#			mgs:v5.1.0/multiplayer/stop [ as @a ]
#			mgs:v5.1.0/missions/start [ as @a ]
#			mgs:v5.1.0/missions/stop [ as @a ]
#

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

