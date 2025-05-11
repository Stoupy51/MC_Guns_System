scoreboard players set v1 V 1
scoreboard players operation v3 V = @s weapon_id
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v3 V run tag @s add curr
scoreboard players set @e[type=minecraft:marker,tag=curr] timestamp 0
execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=0}] run tag @s[scores={carrot_click=1..,cooldown=0},tag=!reloading] add reloading

execute if entity @s[scores={weapon=510..519}] run function mgs:guns/051/handler
execute if entity @s[scores={weapon=520..529}] run function mgs:guns/052/handler
execute if entity @s[scores={weapon=530..539}] run function mgs:guns/053/handler
execute if entity @s[scores={weapon=540..549}] run function mgs:guns/054/handler
execute if entity @s[scores={weapon=550..559}] run function mgs:guns/055/handler
execute if entity @s[scores={weapon=560..569}] run function mgs:guns/056/handler
execute if entity @s[scores={weapon=570..579}] run function mgs:guns/057/handler
execute if entity @s[scores={weapon=580..589}] run function mgs:guns/058/handler
execute if entity @s[scores={weapon=590..599}] run function mgs:guns/059/handler
execute if entity @s[scores={weapon=600..609}] run function mgs:guns/060/handler

tag @e[type=minecraft:marker,tag=curr] remove curr