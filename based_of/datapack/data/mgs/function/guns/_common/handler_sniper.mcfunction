scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=410..419}] run function mgs:guns/041/handler
execute if entity @s[scores={weapon=420..429}] run function mgs:guns/042/handler
execute if entity @s[scores={weapon=430..439}] run function mgs:guns/043/handler
execute if entity @s[scores={weapon=440..449}] run function mgs:guns/044/handler
execute if entity @s[scores={weapon=450..459}] run function mgs:guns/045/handler
execute if entity @s[scores={weapon=460..469}] run function mgs:guns/046/handler
execute if entity @s[scores={weapon=470..479}] run function mgs:guns/047/handler
execute if entity @s[scores={weapon=480..489}] run function mgs:guns/048/handler
execute if entity @s[scores={weapon=490..499}] run function mgs:guns/049/handler
execute if entity @s[scores={weapon=500..509}] run function mgs:guns/050/handler

tag @e[type=minecraft:marker,tag=curr] remove curr