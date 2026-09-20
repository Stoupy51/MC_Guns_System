
#> mgs:v5.1.0/zombies/perks/electric_cherry_hit
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/electric_cherry_damage {scale:"$(scale)"}
#
# @args		scale (string)
#

$execute store result storage mgs:temp _ec_dmg.amount int 1 run attribute @s minecraft:max_health get $(scale)
data modify storage mgs:temp _ec_dmg.type set value "minecraft:lightning_bolt"
particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.1 12
effect give @s minecraft:slowness 60 3 true
function mgs:v5.1.0/zombies/traps/apply_trap_damage with storage mgs:temp _ec_dmg

