scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=210..219}] run function mgs:guns/021/handler
execute if entity @s[scores={weapon=220..229}] run function mgs:guns/022/handler
execute if entity @s[scores={weapon=230..239}] run function mgs:guns/023/handler
execute if entity @s[scores={weapon=240..249}] run function mgs:guns/024/handler
execute if entity @s[scores={weapon=250..259}] run function mgs:guns/025/handler
execute if entity @s[scores={weapon=260..269}] run function mgs:guns/026/handler
execute if entity @s[scores={weapon=270..279}] run function mgs:guns/027/handler
execute if entity @s[scores={weapon=280..289}] run function mgs:guns/028/handler
execute if entity @s[scores={weapon=290..299}] run function mgs:guns/029/handler
execute if entity @s[scores={weapon=300..309}] run function mgs:guns/030/handler

tag @e[type=minecraft:marker,tag=curr] remove curr