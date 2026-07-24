
#> mgs:v5.1.0/zombies/wallbuys/buy_knife
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

# Already own this exact knife: nothing to buy
$execute if items entity @s hotbar.0 *[custom_data~{mgs:{$(weapon_id):true}}] run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.you_already_own_this_knife","color":"yellow"}'}

# Full price
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#wb_price",obj:"mgs.data"}
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data

# Replace the knife slot and re-tag it for the zombies slot enforcement (inventory/check_slots)
$loot replace entity @s hotbar.0 loot mgs:i/$(weapon_id)
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.0",group:"hotbar",index:0}
function mgs:v5.1.0/zombies/wallbuys/msg_purchased

