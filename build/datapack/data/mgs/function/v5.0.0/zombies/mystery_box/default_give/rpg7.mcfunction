
#> mgs:v5.0.0/zombies/mystery_box/default_give/rpg7
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {weapon_id:"rpg7",name:"rpg7"}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

