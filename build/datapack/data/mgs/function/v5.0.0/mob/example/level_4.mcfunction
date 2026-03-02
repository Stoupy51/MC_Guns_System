
#> mgs:v5.0.0/mob/example/level_4
#
# @within	???
#
# @args		entity (unknown)
#

# Summon entity with armed tag and custom name
$summon $(entity) ~ ~ ~ {"Tags":["mgs.armed","mgs.new"],"CustomName":{"text":"Armed $(entity) [Lv.4]","color":"red"}}

# Give a random weapon to the entity
execute as @n[tag=mgs.new] run function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

# Set mob active time and sleep time
scoreboard players set @n[tag=mgs.new] mgs.mob.active_time 72000
scoreboard players set @n[tag=mgs.new] mgs.mob.sleep_time 1

# Clean up new tag
tag @n[tag=mgs.new] remove mgs.new

