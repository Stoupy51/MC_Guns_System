
#> mgs:v5.0.1/zombies/mystery_box/pick_for_buyer
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.0.1/zombies/mystery_box/show_result_one [ as @a[scores={mgs.zb.in_game=1}] ]
#

function mgs:v5.0.1/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll mgs.data 0
function mgs:v5.0.1/zombies/mystery_box/reroll_owned
# Treat a missing result (empty pool / all owned after rerolls) as "owned" so we refund
execute unless data storage mgs:zombies mystery_box.result.weapon_id run scoreboard players set #mb_owned mgs.data 1

