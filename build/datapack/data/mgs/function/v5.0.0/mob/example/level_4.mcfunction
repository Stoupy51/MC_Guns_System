
#> mgs:v5.0.0/mob/example/level_4
#
# @within	???
#

# Summon pillager with armed tag and custom name
summon pillager ~ ~ ~ {"Tags":["mgs.armed","mgs.new"],"CustomName":{"translate": "mgs.armed_pillager_lv_4","color":"red"}}

# Give a random weapon to the pillager
execute as @n[tag=mgs.new] run function mgs:v5.0.0/utils/random_weapon {slot:"weapon.mainhand"}

# Set mob active time to 50 ticks and sleep time to 100 ticks (difficulty 1 equivalent)
scoreboard players set @n[tag=mgs.new] mgs.mob.active_time 72000
scoreboard players set @n[tag=mgs.new] mgs.mob.sleep_time 0

# Clean up new tag
tag @n[tag=mgs.new] remove mgs.new

