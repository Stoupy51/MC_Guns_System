
#> mgs:v5.0.0/mob/default/level_2
#
# @within	???
#
# @args		entity (unknown)
#

# Summon entity with armed tag and custom name
$summon $(entity) ~ ~ ~ {"Tags":["mgs.armed","mgs.new"],"CustomName":{"text":"Armed $(entity) [Lv.2]","color":"red"}}

# Give a random weapon to the entity
execute as @n[tag=mgs.new] run function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

# Set mob active time and sleep time
scoreboard players set @n[tag=mgs.new] mgs.mob.active_time 50
scoreboard players set @n[tag=mgs.new] mgs.mob.sleep_time 50

# Increment armed mob count & Clean up new tag
scoreboard players add #armed_mob_count mgs.data 1
tag @n[tag=mgs.new] remove mgs.new

