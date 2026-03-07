
#> mgs:v5.0.0/mob/default/on_new_lv5
#
# @within	mgs:v5.0.0/mob/default/level_5 {entity:"$(entity)"}
#
# @args		entity (unknown)
#

# Tags, data, and attributes
tag @s add mgs.armed
tag @s add mgs.mob_lv5
$data modify entity @s CustomName set value {"text":"Armed $(entity) [Lv.5]","color":"dark_red","bold":true}
data modify entity @s DeathLootTable set value "minecraft:empty"
data modify entity @s HandDropChances set value [0.2f,0.0f]
data modify entity @s PersistenceRequired set value true
attribute @s minecraft:waypoint_transmit_range base set 32

# Give a random weapon to the entity
function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

# Level 5: always active, never sleeps (perfect accuracy, no inaccuracy rotation)
scoreboard players set @s mgs.mob.active_time 72000
scoreboard players set @s mgs.mob.sleep_time 0

# Increment armed mob count
scoreboard players add #armed_mob_count mgs.data 1

