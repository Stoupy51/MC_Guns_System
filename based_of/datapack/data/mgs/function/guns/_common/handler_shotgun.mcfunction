scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=310..319}] run function mgs:guns/031/handler
execute if entity @s[scores={weapon=320..329}] run function mgs:guns/032/handler
execute if entity @s[scores={weapon=330..339}] run function mgs:guns/033/handler
execute if entity @s[scores={weapon=340..349}] run function mgs:guns/034/handler
execute if entity @s[scores={weapon=350..359}] run function mgs:guns/035/handler
execute if entity @s[scores={weapon=360..369}] run function mgs:guns/036/handler
execute if entity @s[scores={weapon=370..379}] run function mgs:guns/037/handler
execute if entity @s[scores={weapon=380..389}] run function mgs:guns/038/handler
execute if entity @s[scores={weapon=390..399}] run function mgs:guns/039/handler
execute if entity @s[scores={weapon=400..409}] run function mgs:guns/040/handler

tag @e[type=minecraft:marker,tag=curr] remove curr