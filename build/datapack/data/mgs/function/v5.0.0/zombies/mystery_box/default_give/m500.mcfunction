
#> mgs:v5.0.0/zombies/mystery_box/default_give/m500
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"m500",name:"m500",consumable:1b,magazine_id:"m500_shell",mag_count:12}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

