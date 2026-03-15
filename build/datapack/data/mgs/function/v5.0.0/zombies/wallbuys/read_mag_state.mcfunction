
#> mgs:v5.0.0/zombies/wallbuys/read_mag_state
#
# @within	mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.wb_reading_mag] $(slot)
execute store result score #wb_mag_rem mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets
execute store result score #wb_mag_cap mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
kill @s

