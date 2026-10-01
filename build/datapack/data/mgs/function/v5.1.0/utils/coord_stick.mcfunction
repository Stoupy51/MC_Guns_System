
#> mgs:v5.1.0/utils/coord_stick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# So tellraw can target them from the aimed-block context.
tag @s add mgs.coord_stick_user
function #bs.view:at_aimed_block {run:"function mgs:v5.1.0/utils/coord_stick_relative",with:{}}
tag @s remove mgs.coord_stick_user

