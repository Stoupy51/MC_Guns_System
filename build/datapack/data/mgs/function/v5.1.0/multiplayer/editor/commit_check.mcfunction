
#> mgs:v5.1.0/multiplayer/editor/commit_check
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/pick_primary
#			mgs:v5.1.0/multiplayer/editor/pick_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_primary_scope
#			mgs:v5.1.0/multiplayer/editor/pick_secondary_scope
#			mgs:v5.1.0/multiplayer/editor/pick_primary_mags
#			mgs:v5.1.0/multiplayer/editor/pick_secondary_mags
#			mgs:v5.1.0/multiplayer/editor/pick_equip_slot1
#			mgs:v5.1.0/multiplayer/editor/pick_equip_slot2
#			mgs:v5.1.0/multiplayer/editor/toggle_perk
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
execute if score @s mgs.mp.edit_points matches 0.. run return 1

# Over budget: revert and deny
data modify storage mgs:temp editor set from storage mgs:temp _ed_bak
function mgs:v5.1.0/multiplayer/editor/recompute_points
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.not_enough_points_for_that","color":"red"}]
return fail

