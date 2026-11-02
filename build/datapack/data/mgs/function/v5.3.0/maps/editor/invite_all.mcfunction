
#> mgs:v5.3.0/maps/editor/invite_all
#
# @within	string in mgs:v5.3.0/players/list_editor
#

execute unless score @s mgs.mp.map_edit matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_must_be_in_map_editor_to_invite_players","fallback":"You must be in map editor to invite players.","color":"red"}]
execute as @a unless score @s mgs.mp.map_edit matches 1 run function mgs:v5.3.0/players/editor_invite

