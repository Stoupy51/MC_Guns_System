
#> mgs:v5.4.2/zombies/wunderfizz/assign_pid
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/wunderfizz/try_use
#

scoreboard players add #wf_pid_counter mgs.data 1
scoreboard players operation @s mgs.zb.wf_pid = #wf_pid_counter mgs.data

