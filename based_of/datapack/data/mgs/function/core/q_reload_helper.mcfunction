scoreboard players set @s[scores={selector=1..}] selector -1
scoreboard players operation @s[tag=!reloading,tag=!switch,scores={selector=0}] selector = selector_delay S
stopsound @s voice
scoreboard players set @s fire 0
scoreboard players set @s[tag=!switch,tag=reloading] cooldown 0
execute at @s[tag=reloading] run playsound mgs:common.lean_out voice @s ~ ~1000000 ~ 10000000
tag @s[tag=reloading] add rstop
tag @s[tag=reloading] remove reloading
tag @s add curr
item replace entity @s weapon.mainhand with minecraft:carrot_on_a_stick 1
execute as @e[type=item,tag=matched,limit=1] run item modify entity @p[tag=curr] weapon.mainhand mgs:q_reload
tag @s remove curr
kill @e[type=item,tag=matched]