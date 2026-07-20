
#> mgs:v5.1.0/zombies/wallbuys/buy_lethal
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

# Same equipment already in the slot: refill flow
$execute if items entity @s hotbar.7 *[custom_data~{mgs:{$(weapon_id):true}}] run return run function mgs:v5.1.0/zombies/wallbuys/refill_lethal with storage mgs:temp _wb_weapon

# NOTE Widow's Wine (README task 5): once webs exist, a web owner's lethal buy must refill
# web grenades instead of switching the type — branch here on the perk score.
# New purchase (empty slot or different equipment type): full price for 4 fresh ones
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/wallbuys/deny_not_enough_points
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data
$loot replace entity @s hotbar.7 loot mgs:i/$(weapon_id)
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}
function mgs:v5.1.0/zombies/inventory/record_lethal_type
function mgs:v5.1.0/zombies/wallbuys/msg_purchased

