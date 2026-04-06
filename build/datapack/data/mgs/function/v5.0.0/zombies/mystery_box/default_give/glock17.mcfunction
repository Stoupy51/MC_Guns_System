
#> mgs:v5.0.0/zombies/mystery_box/default_give/glock17
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"glock17",name:"glock17",consumable:0b,magazine_id:"glock17_mag",mag_count:2}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

