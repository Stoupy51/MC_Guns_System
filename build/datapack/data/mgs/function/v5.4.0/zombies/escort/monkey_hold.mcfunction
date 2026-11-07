
#> mgs:v5.4.0/zombies/escort/monkey_hold
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/escort/monkey_ride
#			mgs:v5.4.0/zombies/escort/give_up
#

scoreboard players operation @s mgs.zb.escort_ttl %= #20 mgs.data
scoreboard players add @s mgs.zb.escort_ttl 900
scoreboard players set @s mgs.zb.stuck_ticks 0

