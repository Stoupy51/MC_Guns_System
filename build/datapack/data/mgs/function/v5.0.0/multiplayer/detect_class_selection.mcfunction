
#> mgs:v5.0.0/multiplayer/detect_class_selection
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"assault"}}] run scoreboard players set @s mgs.mp.class 1
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"rifleman"}}] run scoreboard players set @s mgs.mp.class 2
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"support"}}] run scoreboard players set @s mgs.mp.class 3
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"sniper"}}] run scoreboard players set @s mgs.mp.class 4
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"smg"}}] run scoreboard players set @s mgs.mp.class 5
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"shotgunner"}}] run scoreboard players set @s mgs.mp.class 6
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"engineer"}}] run scoreboard players set @s mgs.mp.class 7
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"medic"}}] run scoreboard players set @s mgs.mp.class 8
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"marksman"}}] run scoreboard players set @s mgs.mp.class 9
execute if items entity @s weapon.mainhand *[custom_data~{mgs:{class_selector:"heavy"}}] run scoreboard players set @s mgs.mp.class 10

# Clear all class selector items from inventory
clear @s minecraft:poisonous_potato[custom_data~{mgs:{class_selector:{}}}]

# If game active: queue for next respawn, keep selectors in inventory for future
execute if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.0.0/multiplayer/give_class_selectors_gameplay
execute if score @s mgs.mp.class matches 1 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Assault","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 2 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Rifleman","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 3 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Support","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 4 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Sniper","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 5 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"SMG","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 6 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Shotgunner","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 7 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Engineer","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 8 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Medic","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 9 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Marksman","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]
execute if score @s mgs.mp.class matches 10 if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"Heavy","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"}]

# If game not active: apply immediately
execute unless data storage mgs:multiplayer game{state:"active"} run function mgs:v5.0.0/multiplayer/apply_class
execute if score @s mgs.mp.class matches 1 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Assault","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 2 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Rifleman","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 3 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Support","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 4 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Sniper","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 5 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"SMG","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 6 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Shotgunner","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 7 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Engineer","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 8 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Medic","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 9 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Marksman","color":"green","bold":true}]
execute if score @s mgs.mp.class matches 10 unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_selected","color":"white"},{"text":"Heavy","color":"green","bold":true}]

