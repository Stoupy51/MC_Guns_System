execute if score enableHBComp V matches 0 if entity @s[nbt={ActiveEffects:[{Id:21b}]}] run tellraw @a {"text":"MGS [Warn]: detected health boost effect. Switching to health boost compatible mode.","color":"yellow"}
execute if score enableHBComp V matches 0 if entity @s[nbt={ActiveEffects:[{Id:21b}]}] run function mgs:gamerule/health_boost_compatability_enable
execute store result score v3 V run data get entity @s AbsorptionAmount
scoreboard players operation v3 V -= @s health

execute store result score v0 V run attribute @s minecraft:generic.max_health get
execute if score v0 V matches 1024.. run tellraw @a {"text":"MGS [Warn]: max_health >= 1024 are not supported!","color":"yellow"}
scoreboard players operation v2 V = v0 V
scoreboard players operation v0 V += v3 V
scoreboard players operation v0 V += @s damage

execute if score showDeath V matches 1 if score v0 V >= v2 V run function mgs:util/damage_lethal
execute if score showDeath V matches 0 if score v0 V >= v2 V run function mgs:util/damage_lethal_simp
execute if score enableHBComp V matches 1 if score v0 V < v2 V run function mgs:util/damage_nonlethal_old
execute if score enableHBComp V matches 0 if score v0 V < v2 V run function mgs:util/damage_nonlethal

scoreboard players set @s damage 0

scoreboard players operation v0 V = @s hit_by
execute as @a if score @s UID = v0 V run tag @s add killer
execute if score @s UID = @p[tag=killer] UID run tellraw @a {"text":"MGS [Error]: self damage caught in damage!","color":"red"}
tag @a[tag=killer] remove killer