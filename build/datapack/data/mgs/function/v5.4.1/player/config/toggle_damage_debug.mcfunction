
#> mgs:v5.4.1/player/config/toggle_damage_debug
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/config/process
#

# #toggle = 1 when it was off.
execute store success score #toggle mgs.data unless score @s mgs.player.damage_debug matches 1
execute if score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 1
execute unless score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 0
execute if score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],["",{"translate":"mgs.damage_debug","fallback":"Damage Debug"},": "],{"text":"ON","color":"green"},{"text":" ✔","color":"green"}]
execute unless score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],["",{"translate":"mgs.damage_debug","fallback":"Damage Debug"},": "],{"translate":"mgs.off","fallback":"OFF","color":"red"},{"text":" ✘","color":"red"}]

# Reopened, so the new state shows at once.
function mgs:v5.4.1/player/config/menu

