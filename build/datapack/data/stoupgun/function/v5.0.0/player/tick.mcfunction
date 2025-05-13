
#> stoupgun:v5.0.0/player/tick
#
# @within	stoupgun:v5.0.0/tick
#

# If pending clicks, run function
execute if score @s stoupgun.cooldown matches 1.. run scoreboard players remove @s stoupgun.cooldown 1
execute if score @s stoupgun.pending_clicks matches 1.. run function stoupgun:v5.0.0/right_click/handle

