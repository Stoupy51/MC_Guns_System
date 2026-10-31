
#> mgs:v5.3.0/mob/arm
#
# @within	mgs:v5.3.0/mob/default/on_new {entity:"$(entity)",level:$(level),active_time:$(active_time),sleep_time:$(sleep_time)}
#			mgs:v5.3.0/zombies/mob/arm with storage mgs:temp _arm
#
# @args		entity (string)
#			level (int)
#			active_time (int)
#			sleep_time (int)
#

tag @s add mgs.armed
$data modify entity @s CustomName set value [{"text":"","color":"red"},"Armed ",{"translate":"entity.minecraft.$(entity)"}," [Lv.$(level)]"]
data modify entity @s DeathLootTable set value "minecraft:empty"
data modify entity @s drop_chances set value {mainhand:0.0f,offhand:0.0f}
data modify entity @s PersistenceRequired set value true
attribute @s minecraft:waypoint_transmit_range base set 32

$scoreboard players set @s mgs.mob.active_time $(active_time)
$scoreboard players set @s mgs.mob.sleep_time $(sleep_time)

scoreboard players add #armed_mob_count mgs.data 1

