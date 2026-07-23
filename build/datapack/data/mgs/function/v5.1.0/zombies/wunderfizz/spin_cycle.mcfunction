
#> mgs:v5.1.0/zombies/wunderfizz/spin_cycle
#
# @executed	as @e[tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/orb_tick
#

scoreboard players operation #wf_mod mgs.data = @s mgs.zb.wf.anim
scoreboard players operation #wf_mod mgs.data %= #3 mgs.data
execute unless score #wf_mod mgs.data matches 0 run return 0
execute store result score #wf_roll mgs.data run random value 0..13
execute if score #wf_roll mgs.data matches 0 run function mgs:v5.1.0/zombies/wunderfizz/set_model/juggernog
execute if score #wf_roll mgs.data matches 1 run function mgs:v5.1.0/zombies/wunderfizz/set_model/speed_cola
execute if score #wf_roll mgs.data matches 2 run function mgs:v5.1.0/zombies/wunderfizz/set_model/double_tap
execute if score #wf_roll mgs.data matches 3 run function mgs:v5.1.0/zombies/wunderfizz/set_model/quick_revive
execute if score #wf_roll mgs.data matches 4 run function mgs:v5.1.0/zombies/wunderfizz/set_model/mule_kick
execute if score #wf_roll mgs.data matches 5 run function mgs:v5.1.0/zombies/wunderfizz/set_model/stamin_up
execute if score #wf_roll mgs.data matches 6 run function mgs:v5.1.0/zombies/wunderfizz/set_model/phd_flopper
execute if score #wf_roll mgs.data matches 7 run function mgs:v5.1.0/zombies/wunderfizz/set_model/deadshot
execute if score #wf_roll mgs.data matches 8 run function mgs:v5.1.0/zombies/wunderfizz/set_model/timeslip
execute if score #wf_roll mgs.data matches 9 run function mgs:v5.1.0/zombies/wunderfizz/set_model/electric_cherry
execute if score #wf_roll mgs.data matches 10 run function mgs:v5.1.0/zombies/wunderfizz/set_model/tombstone
execute if score #wf_roll mgs.data matches 11 run function mgs:v5.1.0/zombies/wunderfizz/set_model/whos_who
execute if score #wf_roll mgs.data matches 12 run function mgs:v5.1.0/zombies/wunderfizz/set_model/dying_wish
execute if score #wf_roll mgs.data matches 13 run function mgs:v5.1.0/zombies/wunderfizz/set_model/widows_wine
# Electric spin feedback (vanilla sounds): a spark + a short conduit zap each cycle
particle minecraft:electric_spark ~ ~ ~ 0.25 0.3 0.25 0.05 3 force @a[distance=..32]
playsound minecraft:block.conduit.ambient.short ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.5 1.4

