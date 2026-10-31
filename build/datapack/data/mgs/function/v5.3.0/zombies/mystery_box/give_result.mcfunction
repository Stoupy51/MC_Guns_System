
#> mgs:v5.3.0/zombies/mystery_box/give_result
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.3.0/zombies/mystery_box/collect
#

scoreboard players set #wb_price mgs.data 0
execute if data storage mgs:zombies mystery_box.result{weapon_id:"monkey_bomb"} run return run function mgs:v5.3.0/zombies/wallbuys/give_tactical {weapon_id:"monkey_bomb"}

data modify storage mgs:temp _wb_weapon set from storage mgs:zombies mystery_box.result
data modify storage mgs:temp _wb_weapon.name set from storage mgs:zombies mystery_box.result.weapon_id
function mgs:v5.3.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

