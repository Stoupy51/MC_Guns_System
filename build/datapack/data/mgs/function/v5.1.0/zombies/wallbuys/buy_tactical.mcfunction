
#> mgs:v5.1.0/zombies/wallbuys/buy_tactical
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

# Same equipment already in the slot: refill flow
$execute if items entity @s hotbar.6 *[custom_data~{mgs:{$(weapon_id):true}}] run return run function mgs:v5.1.0/zombies/wallbuys/refill_tactical with storage mgs:temp _wb_weapon

# New purchase (empty slot or different equipment type): full price for 3 fresh ones
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#wb_price",obj:"mgs.data"}
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data
$loot replace entity @s hotbar.6 loot mgs:i/$(weapon_id)
item modify entity @s hotbar.6 mgs:v5.1.0/grenade/set_count_3
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.6",group:"hotbar",index:6}
function mgs:v5.1.0/zombies/wallbuys/msg_purchased

