
#> mgs:v5.1.0/zombies/monkey/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick [ at @s ]
#

# Outside a zombies game the monkey is a long-fuse frag.
execute unless data storage mgs:zombies game{state:"active"} run return 0

scoreboard players operation #monkey_phase mgs.data = #total_tick mgs.data
scoreboard players operation #monkey_phase mgs.data %= #20 mgs.data

# Twice a second, nearby zombies are sent to the monkey through the escort taxi.
execute if score #monkey_phase mgs.data matches 0 run function mgs:v5.1.0/zombies/monkey/attract
execute if score #monkey_phase mgs.data matches 10 run function mgs:v5.1.0/zombies/monkey/attract

# Once a second (TODO: real monkey-music .ogg).
execute if score #monkey_phase mgs.data matches 0 run function mgs:v5.1.0/zombies/monkey/pulse

