
#> mgs:v5.1.0/zombies/freeze_on
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/freeze_toggle
#

scoreboard players set #zb_freeze mgs.data 1
function mgs:v5.1.0/zombies/freeze_world

title @a[scores={mgs.zb.in_game=1}] times 5 60 10
title @a[scores={mgs.zb.in_game=1}] title [{"text":"⏸","color":"white"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_froze_the_game","color":"aqua"}]

