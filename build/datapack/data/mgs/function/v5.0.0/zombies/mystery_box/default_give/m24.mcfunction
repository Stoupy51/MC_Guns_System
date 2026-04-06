
#> mgs:v5.0.0/zombies/mystery_box/default_give/m24
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"m24",name:"m24",consumable:1b,magazine_id:"m24_bullet",mag_count:10}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

