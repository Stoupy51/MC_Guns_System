
#> mgs:v5.1.0/zombies/monkey/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick [ at @s ]
#

# Attraction is a zombies-game mechanic only (elsewhere the monkey is just a long-fuse frag)
execute unless data storage mgs:zombies game{state:"active"} run return 0

# Cadence off the global tick counter (main.py increments #total_tick every tick)
scoreboard players operation #monkey_phase mgs.data = #total_tick mgs.data
scoreboard players operation #monkey_phase mgs.data %= #20 mgs.data

# Twice a second: (re)direct nearby zombies to this monkey through the escort taxi
execute if score #monkey_phase mgs.data matches 0 run function mgs:v5.1.0/zombies/monkey/attract
execute if score #monkey_phase mgs.data matches 10 run function mgs:v5.1.0/zombies/monkey/attract

# Once a second: toy-jingle placeholder + note particles (real monkey-music .ogg is a HUMAN asset)
execute if score #monkey_phase mgs.data matches 0 run function mgs:v5.1.0/zombies/monkey/pulse

