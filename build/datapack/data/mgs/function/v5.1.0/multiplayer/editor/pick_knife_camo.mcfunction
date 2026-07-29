
#> mgs:v5.1.0/multiplayer/editor/pick_knife_camo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

execute if score @s mgs.player.config matches 540 run data modify storage mgs:temp editor.knife_camo set value ""
execute if score @s mgs.player.config matches 540 run data modify storage mgs:temp editor.knife_camo_name set value "Default"
execute if score @s mgs.player.config matches 541 run data modify storage mgs:temp editor.knife_camo set value "_autumn"
execute if score @s mgs.player.config matches 541 run data modify storage mgs:temp editor.knife_camo_name set value "Autumn"
execute if score @s mgs.player.config matches 542 run data modify storage mgs:temp editor.knife_camo set value "_galaxy"
execute if score @s mgs.player.config matches 542 run data modify storage mgs:temp editor.knife_camo_name set value "Galaxy"
execute if score @s mgs.player.config matches 543 run data modify storage mgs:temp editor.knife_camo set value "_gold"
execute if score @s mgs.player.config matches 543 run data modify storage mgs:temp editor.knife_camo_name set value "Gold"
execute if score @s mgs.player.config matches 544 run data modify storage mgs:temp editor.knife_camo set value "_red_polymer_stripes"
execute if score @s mgs.player.config matches 544 run data modify storage mgs:temp editor.knife_camo_name set value "Red Polymer"

function mgs:v5.1.0/multiplayer/editor/hub

