
#> mgs:v5.1.0/zombies/wallbuys/buy_lethal_web
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/buy_lethal with storage mgs:temp _wb_weapon
#

execute if items entity @s hotbar.7 *[custom_data~{mgs:{stats:{grenade_type:"web"}}}] run return run function mgs:v5.1.0/zombies/wallbuys/refill_lethal with storage mgs:temp _wb_weapon
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/wallbuys/deny_not_enough_points
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data
loot replace entity @s hotbar.7 loot mgs:i/web_grenade
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}
function mgs:v5.1.0/zombies/wallbuys/msg_purchased

