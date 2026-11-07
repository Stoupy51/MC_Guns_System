
#> mgs:v5.4.0/zombies/traps/apply_timeslip_cd
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/traps/active_tick
#

scoreboard players set #ts_num mgs.data 3
scoreboard players set #ts_den mgs.data 4
scoreboard players operation @s mgs.zb.trap.cd *= #ts_num mgs.data
scoreboard players operation @s mgs.zb.trap.cd /= #ts_den mgs.data

