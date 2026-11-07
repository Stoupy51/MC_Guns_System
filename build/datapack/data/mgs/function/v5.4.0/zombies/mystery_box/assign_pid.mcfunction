
#> mgs:v5.4.0/zombies/mystery_box/assign_pid
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/mystery_box/try_use
#

scoreboard players add #mb_pid_counter mgs.data 1
scoreboard players operation @s mgs.mb.pid = #mb_pid_counter mgs.data

