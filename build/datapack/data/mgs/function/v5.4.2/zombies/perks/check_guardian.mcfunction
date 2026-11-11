
#> mgs:v5.4.2/zombies/perks/check_guardian
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/start_round
#

execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability=2,mgs.zb.ability_cd=0},gamemode=!spectator] at @s run function mgs:v5.4.2/zombies/perks/trigger_guardian

