
#> mgs:v5.1.0/zombies/monkey/on_throw
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.1.0/grenade/init
#

# Tag drives the per-tick attraction hook (grenade/tick) and lets cleanup find monkey grenades
tag @s add mgs.monkey_bomb

# Wind-up cue (placeholder: the real toy-jingle .ogg is a HUMAN asset, see zombies README task 8)
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6

