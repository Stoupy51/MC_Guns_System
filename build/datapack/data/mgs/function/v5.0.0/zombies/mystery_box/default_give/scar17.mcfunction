
#> mgs:v5.0.0/zombies/mystery_box/default_give/scar17
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"scar17",name:"scar17",consumable:0b,mag_id:"scar17_mag",mag_count:3}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon
execute if score #wb_purchase_done mgs.data matches 1 if data storage mgs:temp _wb_weapon{consumable:1b} run function mgs:v5.0.0/zombies/mystery_box/give_consumable_reserve with storage mgs:temp _wb_weapon

