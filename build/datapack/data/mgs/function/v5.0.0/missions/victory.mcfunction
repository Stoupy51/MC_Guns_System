
#> mgs:v5.0.0/missions/victory
#
# @within	mgs:v5.0.0/missions/level_cleared
#

tellraw @a ["",{"text":"","color":"gold","bold":true},"🏆 ",{"translate": "mgs.mission_complete"}]
tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.all_levels_cleared_well_done","color":"green"}]

# End game
function mgs:v5.0.0/missions/stop

