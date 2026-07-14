
#> mgs:v5.1.0/zombies/mystery_box/assign_pid
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/try_use
#

scoreboard players add #mb_pid_counter mgs.data 1
scoreboard players operation @s mgs.mb.pid = #mb_pid_counter mgs.data

