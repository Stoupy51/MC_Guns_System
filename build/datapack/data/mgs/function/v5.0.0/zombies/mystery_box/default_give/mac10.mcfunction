
#> mgs:v5.0.0/zombies/mystery_box/default_give/mac10
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"mac10",name:"mac10",consumable:0b,magazine_id:"mac10_mag",mag_count:4}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

