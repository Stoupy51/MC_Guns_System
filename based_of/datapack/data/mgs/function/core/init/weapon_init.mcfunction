summon minecraft:marker 0 -64 0 {Tags:[wm]}
scoreboard players operation @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] UID = _uid_ptr UID
scoreboard players add _uid_ptr UID 1
scoreboard players set @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] timestamp 0
scoreboard players set @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] selector 0
scoreboard players set @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] lim 2147483647
scoreboard players operation v0 V = @s weapon
scoreboard players operation v0 V /= 10 C
scoreboard players operation @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] weapon = v0 V
data modify storage mgs:tmp Item set from entity @s SelectedItem
execute store result score @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] mag run data get storage mgs:tmp Item.tag.Fill
execute if data storage mgs:tmp Item.tag.Limit store result score @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] lim run data get storage mgs:tmp Item.tag.Limit
data modify storage mgs:tmp Item.tag.Fresh set value 0
execute store result storage mgs:tmp Item.tag.WUID int 1 run scoreboard players get @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] UID
item modify entity @s weapon.mainhand mgs:weapon_init
tag @e[type=minecraft:marker,tag=!ini,tag=wm,limit=1] add ini
function mgs:core/weapon_id