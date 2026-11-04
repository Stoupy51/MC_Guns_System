
#> mgs:v5.3.0/zombies/freeze_off
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/admin/freeze_toggle
#

function mgs:v5.3.0/zombies/unfreeze_world
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.an_operator_unfroze_the_game","fallback":"An operator unfroze the game.","color":"aqua"}]

