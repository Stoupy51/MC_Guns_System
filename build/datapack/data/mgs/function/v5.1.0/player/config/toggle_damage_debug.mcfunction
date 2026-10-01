
#> mgs:v5.1.0/player/config/toggle_damage_debug
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# #toggle = 1 when it was off.
execute store success score #toggle mgs.data unless score @s mgs.player.damage_debug matches 1
execute if score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 1
execute unless score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 0
execute if score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.damage_debug"},": "],{"text":"ON","color":"green"},{"text":" ✔","color":"green"}]
execute unless score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.damage_debug"},": "],{"translate":"mgs.off","color":"red"},{"text":" ✘","color":"red"}]

# Reopened, so the new state shows at once.
function mgs:v5.1.0/player/config/menu

