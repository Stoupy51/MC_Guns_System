
#> mgs:v5.0.0/mob/default/on_new
#
# @within	mgs:v5.0.0/mob/default/level_1 {entity:"$(entity)",level:1,active_time:50,sleep_time:100}
#			mgs:v5.0.0/mob/default/level_2 {entity:"$(entity)",level:2,active_time:50,sleep_time:50}
#			mgs:v5.0.0/mob/default/level_3 {entity:"$(entity)",level:3,active_time:60,sleep_time:20}
#			mgs:v5.0.0/mob/default/level_4 {entity:"$(entity)",level:4,active_time:72000,sleep_time:1}
#
# @args		entity (unknown)
#			level (int)
#			active_time (int)
#			sleep_time (int)
#

# Tags, data, and attributes
tag @s add mgs.armed
$data modify entity @s CustomName set value {"text":"Armed $(entity) [Lv.$(level)]","color":"red"}
data modify entity @s DeathLootTable set value "minecraft:empty"
data modify entity @s HandDropChances set value [0.2f,0.0f]
data modify entity @s PersistenceRequired set value true
attribute @s minecraft:waypoint_transmit_range base set 32

# Give a random weapon to the entity
function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

# Set mob active time and sleep time
$scoreboard players set @s mgs.mob.active_time $(active_time)
$scoreboard players set @s mgs.mob.sleep_time $(sleep_time)

# Increment armed mob count
scoreboard players add #armed_mob_count mgs.data 1

