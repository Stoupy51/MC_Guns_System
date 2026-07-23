
#> mgs:v5.1.0/grenade/detonate_web
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.1.0/grenade/detonate
#

# Webbing burst visuals + sound
particle minecraft:item{item:"minecraft:cobweb"} ~ ~0.5 ~ 1.2 0.8 1.2 0.1 80 force @a[distance=..64]
particle minecraft:block{block_state:"minecraft:cobweb"} ~ ~0.5 ~ 1.5 1 1.5 0.05 40 force @a[distance=..64]
playsound minecraft:block.wool.place player @a[distance=..48] ~ ~ ~ 1 0.7
playsound minecraft:entity.spider.step player @a[distance=..48] ~ ~ ~ 1 0.6

# Root + damage nearby zombies (radius from the grenade's effect radius stat)
execute store result score #web_r mgs.data run data get entity @s data.config.grenade_effect_radius
execute store result storage mgs:temp _web.radius float 1 run scoreboard players get #web_r mgs.data
execute at @s run function mgs:v5.1.0/zombies/perks/widows_web_burst with storage mgs:temp _web

# Delete the grenade
function mgs:v5.1.0/grenade/delete

