
#> mgs:v5.1.0/zombies/horde_ambient
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# Run as an in-game player.
execute store result score #horde_count mgs.data if entity @e[tag=mgs.zombie_round,distance=..32]

# Nothing nearby: wait a full cycle before the next entity scan.
execute if score #horde_count mgs.data matches ..0 run scoreboard players set @s mgs.zb.horde_cd 60
execute if score #horde_count mgs.data matches ..0 run return 0

# Volume (hundredths) 1.00 + count x 0.05, capped at 2.00 (20+ zombies reach the full 32 blocks).
scoreboard players set #horde_vol mgs.data 100
scoreboard players operation #horde_tmp mgs.data = #horde_count mgs.data
scoreboard players operation #horde_tmp mgs.data *= #5 mgs.data
scoreboard players operation #horde_vol mgs.data += #horde_tmp mgs.data
execute if score #horde_vol mgs.data matches 200.. run scoreboard players set #horde_vol mgs.data 200
execute store result storage mgs:temp _horde.vol double 0.01 run scoreboard players get #horde_vol mgs.data

# Sprint channel first, like BO2: the sprinter closing in, one scream at a time (SPRINT_LOCKOUT), never pitch-shifted.
scoreboard players set #horde_sprint mgs.data 0
execute unless score @s mgs.zb.vox_sprint > #total_tick mgs.data store success score #horde_sprint mgs.data at @n[tag=mgs.zb_sprint,tag=mgs.zombie_round,distance=..32,sort=random] run function mgs:v5.1.0/zombies/vocals/horde_sprint with storage mgs:temp _horde
execute if score #horde_sprint mgs.data matches 1 run scoreboard players operation @s mgs.zb.vox_sprint = #total_tick mgs.data
execute if score #horde_sprint mgs.data matches 1 run scoreboard players add @s mgs.zb.vox_sprint 110

# Behind channel: `rotated ~180 0` puts ^ ^ ^3 straight behind the player at their height. Rolled, so it is rare.
execute if score #horde_sprint mgs.data matches 0 store result score #horde_behind_roll mgs.data run random value 1..100
scoreboard players set #horde_behind mgs.data 0
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind_roll mgs.data matches ..25 store success score #horde_behind mgs.data rotated ~180 0 positioned ^ ^ ^3 at @n[tag=mgs.zombie_round,distance=..3.0] run function mgs:v5.1.0/zombies/vocals/horde_behind

# Otherwise a short groan from a random nearby zombie, so it comes from the right direction;
# random pitch 0.70 to 1.05 keeps 6 clips from sounding repetitive.
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 store result score #horde_pitch mgs.data run random value 70..105
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 store result storage mgs:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch mgs.data
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 at @e[tag=mgs.zombie_round,distance=..32,sort=random,limit=1] run function mgs:v5.1.0/zombies/vocals/horde_ambient with storage mgs:temp _horde

# Next vocal in 60 ticks / nearby count: a lone zombie every 3.0 s,
# 2+ zombies at the 2.0 s floor.
scoreboard players operation #horde_next mgs.data = #60 mgs.data
scoreboard players operation #horde_next mgs.data /= #horde_count mgs.data
execute if score #horde_next mgs.data matches ..40 run scoreboard players set #horde_next mgs.data 40
scoreboard players operation @s mgs.zb.horde_cd = #horde_next mgs.data

