
#> mgs:v5.4.2/zoom/crosshair_spread
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/main
#

scoreboard players set #spread mgs.data 1
execute if predicate mgs:v5.4.2/is_moving unless predicate mgs:v5.4.2/is_sprinting run scoreboard players set #spread mgs.data 2
execute if predicate mgs:v5.4.2/is_sprinting run scoreboard players set #spread mgs.data 3
execute if predicate mgs:v5.4.2/is_sneaking run scoreboard players set #spread mgs.data 0
execute unless predicate mgs:v5.4.2/is_on_ground run scoreboard players set #spread mgs.data 4
execute unless predicate mgs:v5.4.2/is_on_ground if predicate mgs:v5.4.2/is_sneaking run scoreboard players set #spread mgs.data 2
function mgs:v5.4.2/zoom/crosshair_apply

