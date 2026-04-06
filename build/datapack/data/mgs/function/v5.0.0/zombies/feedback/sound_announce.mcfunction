
#> mgs:v5.0.0/zombies/feedback/sound_announce
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.0.0/zombies/doors/on_right_click
#			mgs:v5.0.0/zombies/traps/on_right_click
#

playsound minecraft:block.note_block.bit ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 0.9

