
#> mgs:v5.0.0/zombies/mystery_box/default_give/m4a1
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"m4a1",name:"m4a1",consumable:0b,magazine_id:"m4a1_mag",mag_count:3}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

