
#> mgs:v5.1.0/zombies/perks/widows_web_hit
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/widows_web_burst
#

effect give @s minecraft:slowness 5 5 true
effect give @s minecraft:weakness 5 2 true
particle minecraft:item{item:"minecraft:cobweb"} ~ ~0.5 ~ 0.3 0.5 0.3 0.05 8
execute store result storage mgs:temp _ww_dmg.amount int 0.15 run scoreboard players get @s mgs.zb.max_hp
data modify storage mgs:temp _ww_dmg.type set value "minecraft:generic"
function mgs:v5.1.0/zombies/traps/apply_trap_damage with storage mgs:temp _ww_dmg

