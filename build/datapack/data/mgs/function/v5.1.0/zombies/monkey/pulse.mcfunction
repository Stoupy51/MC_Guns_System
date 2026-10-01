
#> mgs:v5.1.0/zombies/monkey/pulse
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/monkey/tick
#

# Chime pitches cycle each pulse, like a little tune (TODO: real monkey-music .ogg).
scoreboard players operation #monkey_note mgs.data = #total_tick mgs.data
scoreboard players operation #monkey_note mgs.data /= #20 mgs.data
scoreboard players operation #monkey_note mgs.data %= #4 mgs.data
execute if score #monkey_note mgs.data matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.7
execute if score #monkey_note mgs.data matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.9
execute if score #monkey_note mgs.data matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.1
execute if score #monkey_note mgs.data matches 3 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.4
particle minecraft:note ~ ~0.5 ~ 0.3 0.3 0.3 1 3 force @a[distance=..32]

