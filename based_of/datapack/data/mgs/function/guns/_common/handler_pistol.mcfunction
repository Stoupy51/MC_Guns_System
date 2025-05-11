scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=110..119}] run function mgs:guns/011/handler
execute if entity @s[scores={weapon=120..129}] run function mgs:guns/012/handler
execute if entity @s[scores={weapon=130..139}] run function mgs:guns/013/handler
execute if entity @s[scores={weapon=140..149}] run function mgs:guns/014/handler
execute if entity @s[scores={weapon=150..159}] run function mgs:guns/015/handler
execute if entity @s[scores={weapon=160..169}] run function mgs:guns/016/handler
execute if entity @s[scores={weapon=170..179}] run function mgs:guns/017/handler
execute if entity @s[scores={weapon=180..189}] run function mgs:guns/018/handler
execute if entity @s[scores={weapon=190..199}] run function mgs:guns/019/handler
execute if entity @s[scores={weapon=200..209}] run function mgs:guns/020/handler

tag @e[type=minecraft:marker,tag=curr] remove curr