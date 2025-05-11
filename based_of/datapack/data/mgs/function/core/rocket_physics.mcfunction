tag @s add cbp
execute as @a if score @s UID = @e[type=minecraft:marker,tag=cbp,limit=1] UID run tag @s add own
execute as @e[type=minecraft:marker,tag=lp] if score @s timestamp = time V if score @s UID = @e[type=minecraft:marker,tag=cbp,limit=1] UID run tag @s add own

scoreboard players operation v1 V = @s dx
scoreboard players operation v2 V = @s dy
scoreboard players operation v3 V = @s dz
scoreboard players set v0 V 1
execute store result score v4 V run data get entity @s Pos[0] 1000
execute store result score v5 V run data get entity @s Pos[1] 1000
execute store result score v6 V run data get entity @s Pos[2] 1000
execute at @s run function mgs:core/rph
execute if score v0 V matches 1 at @s run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..11 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..10 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..9 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..8 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..7 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..6 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..5 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..4 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..3 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..3 run function mgs:core/rph
execute if score v0 V matches 1 at @s if score @s cooldown matches ..1 run function mgs:core/rph
execute if score v0 V matches ..0 run tag @s add dead
execute as @s[tag=dead] at @s run summon creeper ~ 0 ~ {Tags:["boom"],Invulnerable:1,PersistenceRequired:1,Silent:1,NoAI:1,Fuse:0,ExplosionRadius:4b}
execute if entity @s[tag=dead] in overworld run item modify block 0 -64 0 container.1 mgs:rocket_name
execute if entity @s[tag=dead] in overworld run data modify entity @e[type=creeper,tag=!e_ini,tag=boom,limit=1] CustomName set from block 0 -64 0 Items[{Slot:1b}].tag.display.Lore[0]
execute as @s[tag=dead] at @s run tp @e[type=creeper,tag=boom] ^ ^ ^-2.0
execute as @s[tag=dead] at @s positioned ^ ^ ^-2.0 run tag @a[tag=!own,distance=..12.5] add exploded
execute as @s[tag=dead] at @s run particle minecraft:explosion_emitter ~2 ~3 ~ 0 0 0 1 1 force
execute as @s[tag=dead] at @s run particle minecraft:explosion_emitter ~ ~1 ~3 0 0 0 1 1 force
execute as @s[tag=dead] at @s run function mgs:guns/_common/playsound/explosion
execute if entity @s[tag=dead] run tag @e[type=creeper,tag=!e_ini,tag=boom] add e_ini
execute if entity @s[tag=dead] run tag @e[type=creeper,tag=boom] remove boom
execute as @s[tag=dead] at @s positioned ^ ^ ^-2.0 run scoreboard players operation @a[tag=!own,distance=..12.5] hit_by = @s UID
scoreboard players set @p[tag=hit] damage 0
tag @e[tag=own] remove own
tag @e[tag=hit] remove hit
tag @e[type=minecraft:marker,tag=cbp] remove cbp
kill @s[tag=dead]
