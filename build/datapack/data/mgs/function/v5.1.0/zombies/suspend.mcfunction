
#> mgs:v5.1.0/zombies/suspend
#
# @within	mgs:v5.1.0/tick
#

scoreboard players set #zb_freeze mgs.data 2
function mgs:v5.1.0/zombies/freeze_world
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_paused_nobody_in_it_is_online","color":"aqua"}]

