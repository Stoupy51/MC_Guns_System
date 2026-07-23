
#> mgs:v5.1.0/zombies/wunderfizz/move_land
#
# @within	mgs:v5.1.0/zombies/wunderfizz/move_tick
#

scoreboard players set #wf_move_timer mgs.data 0
kill @e[tag=mgs.wf_bear]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_has_arrived_at_a_new_location","color":"yellow"}]
execute as @n[tag=mgs.wf_active] at @s run function mgs:v5.1.0/zombies/feedback/sound_announce

