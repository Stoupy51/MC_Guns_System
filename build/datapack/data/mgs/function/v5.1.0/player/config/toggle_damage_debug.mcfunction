
#> mgs:v5.1.0/player/config/toggle_damage_debug
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Flip the toggle: #toggle = 1 when it was OFF (so we turn it ON), 0 when it was already ON
execute store success score #toggle mgs.data unless score @s mgs.player.damage_debug matches 1
execute if score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 1
execute unless score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.damage_debug 0
execute if score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.damage_debug"},": "],{"text":"ON","color":"green"},{"text":" ✔","color":"green"}]
execute unless score #toggle mgs.data matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.damage_debug"},": "],{"translate":"mgs.off","color":"red"},{"text":" ✘","color":"red"}]

# Reopen the settings dialog so the updated state is reflected immediately
function mgs:v5.1.0/player/config/menu

