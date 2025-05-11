scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=10..19}] run function mgs:guns/001/handler
execute if entity @s[scores={weapon=20..29}] run function mgs:guns/002/handler
execute if entity @s[scores={weapon=30..39}] run function mgs:guns/003/handler
execute if entity @s[scores={weapon=40..49}] run function mgs:guns/004/handler
execute if entity @s[scores={weapon=50..59}] run function mgs:guns/005/handler
execute if entity @s[scores={weapon=60..69}] run function mgs:guns/006/handler
execute if entity @s[scores={weapon=70..79}] run function mgs:guns/007/handler
execute if entity @s[scores={weapon=80..89}] run function mgs:guns/008/handler
execute if entity @s[scores={weapon=90..99}] run function mgs:guns/009/handler
execute if entity @s[scores={weapon=100..109}] run function mgs:guns/010/handler

tag @e[type=minecraft:marker,tag=curr] remove curr