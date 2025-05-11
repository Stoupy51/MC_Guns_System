execute if score enableMagazines V matches 1 store success score v1 V run clear @s clock{CustomModelData:120} 0
execute if score enableMagazines V matches 0 as @e[type=minecraft:marker,tag=curr] if score @s mag >= @s lim run scoreboard players set v1 V 0
execute if score v1 V matches 1 run playsound mgs:m9.reload voice @s[tag=reloading,scores={cooldown=0}] ~ ~1000000 ~ 10000000
execute if score v1 V matches 0 run stopsound @s[tag=reloading] voice mgs:m9.reload
execute if score v1 V matches 0 if score @e[type=minecraft:marker,tag=curr,limit=1] mag matches 0 run playsound mgs:common.empty voice @s[tag=reloading,scores={cooldown=0}] ~ ~1000000 ~ 10000000
execute if score v1 V matches 0 if score @e[type=minecraft:marker,tag=curr,limit=1] mag matches 1.. run playsound mgs:common.lean_out voice @s[tag=reloading,scores={cooldown=0}] ~ ~1000000 ~ 10000000
execute if score v1 V matches 0 run tag @s[tag=reloading] remove reloading

scoreboard players operation v1 V = @e[type=minecraft:marker,tag=curr] mag
scoreboard players operation v2 V = m9_mag S
scoreboard players operation v4 V = @e[type=minecraft:marker,tag=curr] lim
execute if score enableMagazines V matches 0 if score v4 V < max_ammo_limit S run scoreboard players operation v2 V = v4 V
execute if score enableMagazines V matches 0 if score v4 V < max_ammo_limit S run scoreboard players operation v2 V -= v1 V
scoreboard players set v3 V 0
execute if score v4 V matches 0 run scoreboard players set v3 V 1
execute if score enableUI V matches 1 if entity @s[tag=!reloading] run function mgs:guns/_common/hud/handler_s

execute if entity @s[tag=reloading,scores={cooldown=0}] run playsound mgs:m9.playerbegin player @a[distance=0.01..16] ~ ~ ~ 0.3
scoreboard players operation @s[tag=reloading,scores={cooldown=0}] cooldown = m9_reload S
execute if entity @s[tag=reloading] if score @s cooldown = m9_reload_end S run playsound mgs:m9.playerend player @a[distance=0.01..16] ~ ~ ~ 0.3

execute if score enableMagazines V matches 1 if entity @s[scores={cooldown=1},tag=reloading] run function mgs:guns/012/handler_reload
execute if score enableMagazines V matches 0 if entity @s[scores={cooldown=1},tag=reloading] run scoreboard players operation @e[type=minecraft:marker,tag=curr] mag = m9_mag S
execute if score enableMagazines V matches 0 as @e[type=minecraft:marker,tag=curr] if score @s mag > @s lim run scoreboard players operation @s mag = @s lim
tag @s[scores={cooldown=1},tag=reloading] remove reloading

scoreboard players operation v15 V = m9_damage S
scoreboard players operation v14 V = m9_acc_base S
scoreboard players operation v13 V = m9_kick S
scoreboard players operation v12 V = m9_decay S
execute if entity @s[scores={sneaky=1..}] run scoreboard players operation v14 V = m9_acc_sneaky S
execute if entity @s[scores={walk=1..}] run scoreboard players operation v14 V = m9_acc_walk S
execute if entity @s[scores={sprint=1..}] run scoreboard players operation v14 V = m9_acc_sprint S
execute if entity @s[scores={jump=4..}] run scoreboard players operation v14 V = m9_acc_jump S

execute if entity @e[type=minecraft:marker,tag=curr,scores={mag=1..,lim=1..}] if entity @s[scores={carrot_click=1..}] run function mgs:guns/012/handler_fire

playsound mgs:common.lean_in player @s[scores={weapon=120..124,sneaky=1..}] ~ ~1000000 ~ 10000000
playsound mgs:common.lean_out player @s[scores={weapon=125..129,sneaky=0}] ~ ~1000000 ~ 10000000
execute if entity @s[scores={weapon=120..124,sneaky=1..}] run function mgs:guns/_common/switch_in
execute if entity @s[scores={weapon=125..129,sneaky=0}] run function mgs:guns/_common/switch_out
scoreboard players set @s[scores={weapon=125..129}] slow 1