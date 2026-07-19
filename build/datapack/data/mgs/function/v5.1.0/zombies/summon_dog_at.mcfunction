
#> mgs:v5.1.0/zombies/summon_dog_at
#
# @executed	as @e[tag=mgs.dog_portal] & at @s
#
# @within	mgs:v5.1.0/zombies/dog_portal_strike
#

# Delivered by the bolt at ground level, AI live immediately — no rise animation, so no zb_rising.
# zb_dog_new is a scratch tag the strike removes once setup is done.
summon minecraft:wolf ~ ~ ~ {Tags:["mgs.zombie_round","mgs.zb_dog","mgs.zb_dog_new","mgs.gm_entity","mgs.nukable"],variant:"minecraft:black",PersistenceRequired:true,DeathLootTable:"minecraft:empty",Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.gm_entity"]}],Attributes:[{id:"minecraft:follow_range",base:40.0d}]}

# Apply scaling (health, speed). Not a macro call: types/dog reads #zb_round itself and never used
# the level argument, so passing one only added a way for the call to be skipped.
execute as @n[tag=mgs.zb_dog_new] run function mgs:v5.1.0/zombies/types/dog

# Ally with escort traders, same reason as zombies (escort.py)
team join mgs.horde @n[tag=mgs.zb_dog_new]

# Initialize stuck detection scores (timestamp + XZ snapshot + distance bucket at spawn)
execute as @n[tag=mgs.zb_dog_new] run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute as @n[tag=mgs.zb_dog_new] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zb_dog_new] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag=mgs.zb_dog_new] mgs.zb.stuck_dist 4

