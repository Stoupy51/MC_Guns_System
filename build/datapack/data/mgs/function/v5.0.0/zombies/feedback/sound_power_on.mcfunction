
#> mgs:v5.0.0/zombies/feedback/sound_power_on
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.0.0/zombies/power/on_activate
#

playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.9 1.0

