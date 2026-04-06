
#> mgs:v5.0.0/zombies/mystery_box/default_give/glock18
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"glock18",name:"glock18",consumable:0b,magazine_id:"glock18_mag",mag_count:2}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

