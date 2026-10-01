
#> mgs:v5.1.0/zombies/monkey/on_throw
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.1.0/grenade/init
#

# Read by the attraction hook (grenade/tick) and by cleanup.
tag @s add mgs.monkey_bomb

# TODO: placeholder until the real toy-jingle .ogg exists.
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6

