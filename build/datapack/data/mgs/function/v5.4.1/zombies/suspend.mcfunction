
#> mgs:v5.4.1/zombies/suspend
#
# @within	mgs:v5.4.1/tick
#			mgs:v5.4.1/dialog/close_then
#

scoreboard players set #zb_freeze mgs.data 2
function mgs:v5.4.1/zombies/freeze_world
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombies_game_paused_nobody_in_it_is_online","fallback":"Zombies game paused: nobody in it is online.","color":"aqua"}]

