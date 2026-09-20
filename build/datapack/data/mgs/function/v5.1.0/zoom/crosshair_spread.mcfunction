
#> mgs:v5.1.0/zoom/crosshair_spread
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/main
#

scoreboard players set #spread mgs.data 1
execute if predicate mgs:v5.1.0/is_moving unless predicate mgs:v5.1.0/is_sprinting run scoreboard players set #spread mgs.data 2
execute if predicate mgs:v5.1.0/is_sprinting run scoreboard players set #spread mgs.data 3
execute if predicate mgs:v5.1.0/is_sneaking run scoreboard players set #spread mgs.data 0
execute unless predicate mgs:v5.1.0/is_on_ground run scoreboard players set #spread mgs.data 4
execute unless predicate mgs:v5.1.0/is_on_ground if predicate mgs:v5.1.0/is_sneaking run scoreboard players set #spread mgs.data 2

execute unless score @s mgs.cross_to matches -2147483648.. run return run function mgs:v5.1.0/zoom/crosshair_first
execute if score @s mgs.cross_to = #spread mgs.data run return 0
function mgs:v5.1.0/zoom/crosshair_swap

