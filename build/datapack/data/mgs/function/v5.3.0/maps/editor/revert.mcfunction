
#> mgs:v5.3.0/maps/editor/revert
#
# @within	string in mgs:v5.3.0/maps/editor/removed_message {id:$(id)}
#
# @args		id (unknown)
#

execute unless score @s mgs.mp.map_edit matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_must_be_in_the_map_editor_to_revert","fallback":"You must be in the map editor to revert.","color":"red"}]
data remove storage mgs:temp _ed_revert
$data modify storage mgs:temp _ed_revert set from storage mgs:temp map_edit.removed[{id:$(id)}].marker
execute unless data storage mgs:temp _ed_revert run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.already_restored_or_too_old_to_revert","fallback":"Already restored, or too old to revert.","color":"yellow"}]
$data remove storage mgs:temp map_edit.removed[{id:$(id)}]

execute summon minecraft:marker run function mgs:v5.3.0/maps/editor/revert_marker
function mgs:v5.3.0/maps/editor/refresh_displays

