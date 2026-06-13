
#> mgs:v5.0.1/multiplayer/editor/toggle_perk
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/pick_perk with storage mgs:temp
#
# @args		_toggle_perk (unknown)
#

# Already selected → remove it (recompute refunds automatically)
$execute if data storage mgs:temp editor{perks:["$(_toggle_perk)"]} run return run function mgs:v5.0.1/multiplayer/editor/remove_perk

# Check max perks limit
execute store result score #perk_count mgs.data run data get storage mgs:temp editor.perks
execute if score #perk_count mgs.data matches 3.. run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.max_3_perks_allowed","color":"red"}]

# Snapshot, add, commit (reverts on overflow)
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
$data modify storage mgs:temp editor.perks append value "$(_toggle_perk)"
execute store success score #ed_ok mgs.data run function mgs:v5.0.1/multiplayer/editor/commit_check

