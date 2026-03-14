
#> mgs:v5.0.0/player/config/toggle_hitmarker
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# If currently OFF (0), turn ON (1)
execute store success score #toggle mgs.data unless score @s mgs.player.hitmarker matches 1
execute if score #toggle mgs.data matches 1 run scoreboard players set @s mgs.player.hitmarker 1
execute if score #toggle mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.hitmarker_sound"},": "],{"text":"ON","color":"green"},{"text":" ✔","color":"green"}]

# Otherwise it was ON, turn OFF
scoreboard players set @s mgs.player.hitmarker 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"translate":"mgs.hitmarker_sound"},": "],{"translate":"mgs.off","color":"red"},{"text":" ✘","color":"red"}]

