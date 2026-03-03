
#> mgs:v5.0.0/multiplayer/editor/pick_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary weapon choice based on trigger value
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary set value "m1911"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_name set value "M1911"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_mag set value "m1911_mag"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_full set value "m1911"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary set value "m9"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_name set value "M9"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_mag set value "m9_mag"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_full set value "m9"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary set value "deagle"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_name set value "Deagle"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_mag set value "deagle_mag"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_full set value "deagle"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary set value "makarov"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_name set value "Makarov"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_mag set value "makarov_mag"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_full set value "makarov"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary set value "glock17"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_name set value "Glock 17"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_mag set value "glock17_mag"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_full set value "glock17"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary set value "glock18"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_name set value "Glock 18"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_mag set value "glock18_mag"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_full set value "glock18"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary set value "vz61"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_name set value "VZ-61"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_mag set value "vz61_mag"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_full set value "vz61"
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary set value ""
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary_name set value "None"
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary_scope_name set value ""
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary_full set value ""

# Route: deagle → scope dialog, others → equipment dialog
execute if data storage mgs:temp editor{secondary:"deagle"} run return run function mgs:v5.0.0/multiplayer/editor/scope/secondary_4only

# No scope variants: go directly to equipment selection
function mgs:v5.0.0/multiplayer/editor/show_equipment_dialog

