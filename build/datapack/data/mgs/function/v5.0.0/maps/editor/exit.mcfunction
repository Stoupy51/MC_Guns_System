
#> mgs:v5.0.0/maps/editor/exit
#
# @within	???
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail
function mgs:v5.0.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.exited_map_editor_changes_discarded","color":"red"}]

