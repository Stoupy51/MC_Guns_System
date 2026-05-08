
#> mgs:v5.0.1/utils/coord_stick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/tick
#

# Tag the player so tellraw can target them from inside the at-aimed-block context
tag @s add mgs.coord_stick_user
function #bs.view:at_aimed_block {run:"function mgs:v5.0.1/utils/coord_stick_relative",with:{}}
tag @s remove mgs.coord_stick_user

