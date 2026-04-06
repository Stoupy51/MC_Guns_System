
#> mgs:v5.0.0/zombies/mystery_box/default_give/m590
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"m590",name:"m590",consumable:1b,magazine_id:"m590_shell",mag_count:16}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

