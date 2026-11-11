
#> mgs:v5.4.2/multiplayer/editor/pick_secondary_camo
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/process
#

execute if score @s mgs.player.config matches 490 run data modify storage mgs:temp editor.secondary_camo set value ""
execute if score @s mgs.player.config matches 490 run data modify storage mgs:temp editor.secondary_camo_name set value "Default"
execute if score @s mgs.player.config matches 491 run data modify storage mgs:temp editor.secondary_camo set value "_autumn"
execute if score @s mgs.player.config matches 491 run data modify storage mgs:temp editor.secondary_camo_name set value "Autumn"
execute if score @s mgs.player.config matches 492 run data modify storage mgs:temp editor.secondary_camo set value "_galaxy"
execute if score @s mgs.player.config matches 492 run data modify storage mgs:temp editor.secondary_camo_name set value "Galaxy"
execute if score @s mgs.player.config matches 493 run data modify storage mgs:temp editor.secondary_camo set value "_gold"
execute if score @s mgs.player.config matches 493 run data modify storage mgs:temp editor.secondary_camo_name set value "Gold"
execute if score @s mgs.player.config matches 494 run data modify storage mgs:temp editor.secondary_camo set value "_red_polymer_stripes"
execute if score @s mgs.player.config matches 494 run data modify storage mgs:temp editor.secondary_camo_name set value "Red Polymer"

function mgs:v5.4.2/multiplayer/editor/set_secondary_full with storage mgs:temp editor
function mgs:v5.4.2/multiplayer/editor/hub

