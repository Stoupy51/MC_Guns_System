
#> mgs:v5.0.1/multiplayer/editor/pick_primary_camo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Store camo choice (free)
execute if score @s mgs.player.config matches 480 run data modify storage mgs:temp editor.primary_camo set value ""
execute if score @s mgs.player.config matches 480 run data modify storage mgs:temp editor.primary_camo_name set value "Default"
execute if score @s mgs.player.config matches 481 run data modify storage mgs:temp editor.primary_camo set value "_autumn"
execute if score @s mgs.player.config matches 481 run data modify storage mgs:temp editor.primary_camo_name set value "Autumn"
execute if score @s mgs.player.config matches 482 run data modify storage mgs:temp editor.primary_camo set value "_galaxy"
execute if score @s mgs.player.config matches 482 run data modify storage mgs:temp editor.primary_camo_name set value "Galaxy"
execute if score @s mgs.player.config matches 483 run data modify storage mgs:temp editor.primary_camo set value "_gold"
execute if score @s mgs.player.config matches 483 run data modify storage mgs:temp editor.primary_camo_name set value "Gold"
execute if score @s mgs.player.config matches 484 run data modify storage mgs:temp editor.primary_camo set value "_red_polymer_stripes"
execute if score @s mgs.player.config matches 484 run data modify storage mgs:temp editor.primary_camo_name set value "Red Polymer"

# Compute full weapon ID (base + scope + camo)
function mgs:v5.0.1/multiplayer/editor/set_primary_full with storage mgs:temp editor

# Show primary mag count dialog
function mgs:v5.0.1/multiplayer/editor/show_primary_mags_dialog

