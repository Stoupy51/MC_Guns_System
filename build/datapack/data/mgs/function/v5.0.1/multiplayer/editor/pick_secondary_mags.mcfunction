
#> mgs:v5.0.1/multiplayer/editor/pick_secondary_mags
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Guard: the gun must be selected (hub grays this out, but triggers can be sent manually)
execute if data storage mgs:temp editor{secondary:""} run return run function mgs:v5.0.1/multiplayer/editor/hub
# Snapshot, apply, commit (reverts on overflow), back to hub
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 396 run data modify storage mgs:temp editor.secondary_mag_count set value 0
execute if score @s mgs.player.config matches 397 run data modify storage mgs:temp editor.secondary_mag_count set value 1
execute if score @s mgs.player.config matches 398 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 399 run data modify storage mgs:temp editor.secondary_mag_count set value 3
execute if score @s mgs.player.config matches 400 run data modify storage mgs:temp editor.secondary_mag_count set value 4
execute if score @s mgs.player.config matches 401 run data modify storage mgs:temp editor.secondary_mag_count set value 5

execute store success score #ed_ok mgs.data run function mgs:v5.0.1/multiplayer/editor/commit_check
function mgs:v5.0.1/multiplayer/editor/hub

