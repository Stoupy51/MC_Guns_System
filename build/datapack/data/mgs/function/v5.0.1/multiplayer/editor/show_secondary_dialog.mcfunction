
#> mgs:v5.0.1/multiplayer/editor/show_secondary_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

execute if data storage mgs:temp editor{perks:["overkill"]} run return run function mgs:v5.0.1/multiplayer/editor/show_secondary_overkill_dialog
function mgs:v5.0.1/multiplayer/editor/show_secondary_pistol_dialog

