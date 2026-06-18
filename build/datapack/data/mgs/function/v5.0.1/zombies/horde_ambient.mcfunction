
#> mgs:v5.0.1/zombies/horde_ambient
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ at @s ]
#

# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count mgs.data if entity @e[tag=mgs.zombie_round,distance=..32]
execute if score #horde_count mgs.data matches ..0 run return 0

# Volume (hundredths) = 0.25 + count*0.03, hard-capped at 0.80 (so ~18+ zombies all sound the same).
scoreboard players set #horde_vol mgs.data 25
scoreboard players operation #horde_tmp mgs.data = #horde_count mgs.data
scoreboard players operation #horde_tmp mgs.data *= #3 mgs.data
scoreboard players operation #horde_vol mgs.data += #horde_tmp mgs.data
execute if score #horde_vol mgs.data matches 80.. run scoreboard players set #horde_vol mgs.data 80

# Random pitch 0.70..1.05 for variety so the loop doesn't sound metronomic.
execute store result score #horde_pitch mgs.data run random value 70..105

# Hand volume/pitch to the macro as doubles (value/100).
execute store result storage mgs:temp _horde.vol double 0.01 run scoreboard players get #horde_vol mgs.data
execute store result storage mgs:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch mgs.data

# Play the groan FROM a random nearby zombie's position (positional audio), so the player hears
# the horde coming from the right direction/distance rather than centred on themselves.
execute at @e[tag=mgs.zombie_round,distance=..32,sort=random,limit=1] run function mgs:v5.0.1/zombies/horde_ambient_play with storage mgs:temp _horde

