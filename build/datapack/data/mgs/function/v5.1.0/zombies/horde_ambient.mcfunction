
#> mgs:v5.1.0/zombies/horde_ambient
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count mgs.data if entity @e[tag=mgs.zombie_round,distance=..32]

# Nothing nearby: wait a full cycle before paying for another entity scan.
execute if score #horde_count mgs.data matches ..0 run scoreboard players set @s mgs.zb.horde_cd 60
execute if score #horde_count mgs.data matches ..0 run return 0

# Volume (hundredths) = 1.00 + count*0.05, capped at 2.00 (20+ zombies all reach the full 32 blocks).
scoreboard players set #horde_vol mgs.data 100
scoreboard players operation #horde_tmp mgs.data = #horde_count mgs.data
scoreboard players operation #horde_tmp mgs.data *= #5 mgs.data
scoreboard players operation #horde_vol mgs.data += #horde_tmp mgs.data
execute if score #horde_vol mgs.data matches 200.. run scoreboard players set #horde_vol mgs.data 200
execute store result storage mgs:temp _horde.vol double 0.01 run scoreboard players get #horde_vol mgs.data

# Sprint channel first. BO2 leads with the sprinter that is closing on you rather than a random member
# of the horde, and the channel lockout is what keeps it to one scream at a time (see SPRINT_LOCKOUT).
# The scream is NOT pitch-shifted: bending a 4-second human scream is instantly audible as a gimmick.
scoreboard players set #horde_sprint mgs.data 0
execute unless score @s mgs.zb.vox_sprint > #total_tick mgs.data store success score #horde_sprint mgs.data at @n[tag=mgs.zb_sprint,tag=mgs.zombie_round,distance=..32,sort=random] run function mgs:v5.1.0/zombies/vocals/horde_sprint with storage mgs:temp _horde
execute if score #horde_sprint mgs.data matches 1 run scoreboard players operation @s mgs.zb.vox_sprint = #total_tick mgs.data
execute if score #horde_sprint mgs.data matches 1 run scoreboard players add @s mgs.zb.vox_sprint 70

# Behind channel, next. `rotated ~180 0` flips the player's yaw and flattens the pitch, so ^ ^ ^3
# lands 3 blocks straight back from them at their own height — which is what makes this "same floor,
# actually behind" rather than "anywhere within N blocks". Rolled, because the whole point of the
# category is to be missed most of the time.
execute if score #horde_sprint mgs.data matches 0 store result score #horde_behind_roll mgs.data run random value 1..100
scoreboard players set #horde_behind mgs.data 0
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind_roll mgs.data matches ..25 store success score #horde_behind mgs.data rotated ~180 0 positioned ^ ^ ^3 at @n[tag=mgs.zombie_round,distance=..3.0] run function mgs:v5.1.0/zombies/vocals/horde_behind

# Otherwise the short groan set, from a random nearby zombie so the horde comes from the right
# direction and distance rather than being centred on the player. Random pitch 0.70..1.05 keeps a
# 6-clip set from sounding metronomic over a long round.
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 store result score #horde_pitch mgs.data run random value 70..105
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 store result storage mgs:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch mgs.data
execute if score #horde_sprint mgs.data matches 0 if score #horde_behind mgs.data matches 0 at @e[tag=mgs.zombie_round,distance=..32,sort=random,limit=1] run function mgs:v5.1.0/zombies/vocals/horde_ambient with storage mgs:temp _horde

# Schedule this player's next vocal: 60 ticks divided by the nearby count, so a lone
# zombie groans every 3.0s and 2+ zombies sit at the 40-tick (2.0s) floor.
# Density then shows up as volume/reach rather than as rate, which is the point of the floor.
scoreboard players operation #horde_next mgs.data = #60 mgs.data
scoreboard players operation #horde_next mgs.data /= #horde_count mgs.data
execute if score #horde_next mgs.data matches ..40 run scoreboard players set #horde_next mgs.data 40
scoreboard players operation @s mgs.zb.horde_cd = #horde_next mgs.data

