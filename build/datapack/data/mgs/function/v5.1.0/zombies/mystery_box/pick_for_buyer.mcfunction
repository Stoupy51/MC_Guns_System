
#> mgs:v5.1.0/zombies/mystery_box/pick_for_buyer
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_result_one [ as @a[scores={mgs.zb.in_game=1}] ]
#

function mgs:v5.1.0/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll mgs.data 0
function mgs:v5.1.0/zombies/mystery_box/reroll_owned
# No result (empty pool, or everything owned after the re-rolls) counts as owned, so the buyer is refunded.
execute unless data storage mgs:zombies mystery_box.result.weapon_id run scoreboard players set #mb_owned mgs.data 1

