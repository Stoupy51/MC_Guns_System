scoreboard players operation v10 V = @s hit_by
scoreboard players operation v11 V = @s UID

gamerule showDeathMessages false
kill @s
execute as @e[type=minecraft:marker,tag=lp] if score @s UID = v11 V run kill @s
tag @s add dead
gamerule showDeathMessages true

execute as @a if score @s UID = v10 V run tag @s add killer
# add custom death messages here:

# be sure to exclude that weapon from the general death message here:
execute if entity @s[tag=hs] if entity @p[tag=killer] run tellraw @a ["",{"selector":"@p[tag=killer]"},{"text":" BOOM headshot "},{"selector":"@s"},{"text":"!"}]
execute if entity @s[tag=!hs] if entity @p[tag=killer] run tellraw @a ["",{"selector":"@p[tag=killer]"},{"text":" clocked "},{"selector":"@s"}]

execute if score @s hit_by matches 0 run tellraw @a ["",{"text":"Killed "},{"selector":"@s"}]

scoreboard players add @p[tag=killer] kills 1
scoreboard players add @p[tag=killer] gunkills 1
tag @a[tag=killer] remove killer