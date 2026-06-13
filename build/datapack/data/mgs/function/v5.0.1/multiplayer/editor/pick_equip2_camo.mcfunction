
#> mgs:v5.0.1/multiplayer/editor/pick_equip2_camo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

execute if score @s mgs.player.config matches 510 run data modify storage mgs:temp editor.equip_slot2_camo set value ""
execute if score @s mgs.player.config matches 510 run data modify storage mgs:temp editor.equip_slot2_camo_name set value "Default"
execute if score @s mgs.player.config matches 511 run data modify storage mgs:temp editor.equip_slot2_camo set value "_autumn"
execute if score @s mgs.player.config matches 511 run data modify storage mgs:temp editor.equip_slot2_camo_name set value "Autumn"
execute if score @s mgs.player.config matches 512 run data modify storage mgs:temp editor.equip_slot2_camo set value "_galaxy"
execute if score @s mgs.player.config matches 512 run data modify storage mgs:temp editor.equip_slot2_camo_name set value "Galaxy"
execute if score @s mgs.player.config matches 513 run data modify storage mgs:temp editor.equip_slot2_camo set value "_gold"
execute if score @s mgs.player.config matches 513 run data modify storage mgs:temp editor.equip_slot2_camo_name set value "Gold"
execute if score @s mgs.player.config matches 514 run data modify storage mgs:temp editor.equip_slot2_camo set value "_red_polymer_stripes"
execute if score @s mgs.player.config matches 514 run data modify storage mgs:temp editor.equip_slot2_camo_name set value "Red Polymer"

function mgs:v5.0.1/multiplayer/editor/hub

