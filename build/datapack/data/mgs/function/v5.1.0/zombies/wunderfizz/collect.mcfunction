
#> mgs:v5.1.0/zombies/wunderfizz/collect
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/machine_click
#

scoreboard players operation #wf_pick mgs.data = @n[tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.perk
execute if score #wf_pick mgs.data matches 0 run function mgs:v5.1.0/zombies/wunderfizz/grant/juggernog
execute if score #wf_pick mgs.data matches 1 run function mgs:v5.1.0/zombies/wunderfizz/grant/speed_cola
execute if score #wf_pick mgs.data matches 2 run function mgs:v5.1.0/zombies/wunderfizz/grant/double_tap
execute if score #wf_pick mgs.data matches 3 run function mgs:v5.1.0/zombies/wunderfizz/grant/quick_revive
execute if score #wf_pick mgs.data matches 4 run function mgs:v5.1.0/zombies/wunderfizz/grant/mule_kick
execute if score #wf_pick mgs.data matches 5 run function mgs:v5.1.0/zombies/wunderfizz/grant/stamin_up
execute if score #wf_pick mgs.data matches 6 run function mgs:v5.1.0/zombies/wunderfizz/grant/phd_flopper
execute if score #wf_pick mgs.data matches 7 run function mgs:v5.1.0/zombies/wunderfizz/grant/deadshot
execute if score #wf_pick mgs.data matches 8 run function mgs:v5.1.0/zombies/wunderfizz/grant/timeslip
execute if score #wf_pick mgs.data matches 9 run function mgs:v5.1.0/zombies/wunderfizz/grant/electric_cherry
execute if score #wf_pick mgs.data matches 10 run function mgs:v5.1.0/zombies/wunderfizz/grant/tombstone
execute if score #wf_pick mgs.data matches 11 run function mgs:v5.1.0/zombies/wunderfizz/grant/whos_who
execute if score #wf_pick mgs.data matches 12 run function mgs:v5.1.0/zombies/wunderfizz/grant/dying_wish
execute if score #wf_pick mgs.data matches 13 run function mgs:v5.1.0/zombies/wunderfizz/grant/widows_wine
kill @n[tag=mgs.wunderfizz_orb,distance=..3]
function mgs:v5.1.0/zombies/feedback/sound_success

