
#> mgs:v5.0.0/maps/editor/delete
#
# @within	???
#
# @args		idx (unknown)
#

# Delete map at given index (called via /function with {idx:N})
$data remove storage mgs:maps multiplayer[$(idx)]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_deleted","color":"red"}]

# Refresh menu
function mgs:v5.0.0/maps/editor/menu

