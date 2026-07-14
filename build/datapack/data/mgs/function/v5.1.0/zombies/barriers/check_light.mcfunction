
#> mgs:v5.1.0/zombies/barriers/check_light
#
# @executed	positioned ~ ~ ~
#
# @within	mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~ ~ ~ ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~ ~1 ~ ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~ ~-1 ~ ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~1 ~ ~ ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~-1 ~ ~ ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~ ~ ~1 ]
#			mgs:v5.1.0/zombies/barriers/compute_brightness [ positioned ~ ~ ~-1 ]
#

# Check light level at current position and update #light if higher
execute if score #light mgs.data matches ..0 if predicate mgs:v5.1.0/light/1 run return run scoreboard players set #light mgs.data 1
execute if score #light mgs.data matches ..1 if predicate mgs:v5.1.0/light/2 run return run scoreboard players set #light mgs.data 2
execute if score #light mgs.data matches ..2 if predicate mgs:v5.1.0/light/3 run return run scoreboard players set #light mgs.data 3
execute if score #light mgs.data matches ..3 if predicate mgs:v5.1.0/light/4 run return run scoreboard players set #light mgs.data 4
execute if score #light mgs.data matches ..4 if predicate mgs:v5.1.0/light/5 run return run scoreboard players set #light mgs.data 5
execute if score #light mgs.data matches ..5 if predicate mgs:v5.1.0/light/6 run return run scoreboard players set #light mgs.data 6
execute if score #light mgs.data matches ..6 if predicate mgs:v5.1.0/light/7 run return run scoreboard players set #light mgs.data 7
execute if score #light mgs.data matches ..7 if predicate mgs:v5.1.0/light/8 run return run scoreboard players set #light mgs.data 8
execute if score #light mgs.data matches ..8 if predicate mgs:v5.1.0/light/9 run return run scoreboard players set #light mgs.data 9
execute if score #light mgs.data matches ..9 if predicate mgs:v5.1.0/light/10 run return run scoreboard players set #light mgs.data 10
execute if score #light mgs.data matches ..10 if predicate mgs:v5.1.0/light/11 run return run scoreboard players set #light mgs.data 11
execute if score #light mgs.data matches ..11 if predicate mgs:v5.1.0/light/12 run return run scoreboard players set #light mgs.data 12
execute if score #light mgs.data matches ..12 if predicate mgs:v5.1.0/light/13 run return run scoreboard players set #light mgs.data 13
execute if score #light mgs.data matches ..13 if predicate mgs:v5.1.0/light/14 run return run scoreboard players set #light mgs.data 14
execute if score #light mgs.data matches ..14 if predicate mgs:v5.1.0/light/15 run return run scoreboard players set #light mgs.data 15

