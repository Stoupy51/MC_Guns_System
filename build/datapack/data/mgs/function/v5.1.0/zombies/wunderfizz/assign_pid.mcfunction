
#> mgs:v5.1.0/zombies/wunderfizz/assign_pid
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/try_use
#

scoreboard players add #wf_pid_counter mgs.data 1
scoreboard players operation @s mgs.zb.wf_pid = #wf_pid_counter mgs.data

