
#> mgs:v5.1.0/zombies/freeze_off
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/freeze_toggle
#

function mgs:v5.1.0/zombies/unfreeze_world
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_unfroze_the_game","color":"aqua"}]

