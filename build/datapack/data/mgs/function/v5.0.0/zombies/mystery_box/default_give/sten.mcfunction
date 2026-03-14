
#> mgs:v5.0.0/zombies/mystery_box/default_give/sten
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"sten",name:"sten"}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

