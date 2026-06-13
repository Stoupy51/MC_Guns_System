
#> mgs:v5.0.1/multiplayer/editor/pick_equip1_camo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

execute if score @s mgs.player.config matches 500 run data modify storage mgs:temp editor.equip_slot1_camo set value ""
execute if score @s mgs.player.config matches 500 run data modify storage mgs:temp editor.equip_slot1_camo_name set value "Default"
execute if score @s mgs.player.config matches 501 run data modify storage mgs:temp editor.equip_slot1_camo set value "_autumn"
execute if score @s mgs.player.config matches 501 run data modify storage mgs:temp editor.equip_slot1_camo_name set value "Autumn"
execute if score @s mgs.player.config matches 502 run data modify storage mgs:temp editor.equip_slot1_camo set value "_galaxy"
execute if score @s mgs.player.config matches 502 run data modify storage mgs:temp editor.equip_slot1_camo_name set value "Galaxy"
execute if score @s mgs.player.config matches 503 run data modify storage mgs:temp editor.equip_slot1_camo set value "_gold"
execute if score @s mgs.player.config matches 503 run data modify storage mgs:temp editor.equip_slot1_camo_name set value "Gold"
execute if score @s mgs.player.config matches 504 run data modify storage mgs:temp editor.equip_slot1_camo set value "_red_polymer_stripes"
execute if score @s mgs.player.config matches 504 run data modify storage mgs:temp editor.equip_slot1_camo_name set value "Red Polymer"

function mgs:v5.0.1/multiplayer/editor/hub

