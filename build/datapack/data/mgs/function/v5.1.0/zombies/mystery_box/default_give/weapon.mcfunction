
#> mgs:v5.1.0/zombies/mystery_box/default_give/weapon
#
# @within	???
#

data modify storage mgs:temp _wb_weapon set value {}
data modify storage mgs:temp _wb_weapon.weapon_id set from storage mgs:zombies mystery_box.result.weapon_id
data modify storage mgs:temp _wb_weapon.name set from storage mgs:zombies mystery_box.result.weapon_id
data modify storage mgs:temp _wb_weapon.consumable set from storage mgs:zombies mystery_box.result.consumable
data modify storage mgs:temp _wb_weapon.magazine_id set from storage mgs:zombies mystery_box.result.magazine_id
data modify storage mgs:temp _wb_weapon.mag_count set from storage mgs:zombies mystery_box.result.mag_count
scoreboard players set #wb_price mgs.data 0
function mgs:v5.1.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

