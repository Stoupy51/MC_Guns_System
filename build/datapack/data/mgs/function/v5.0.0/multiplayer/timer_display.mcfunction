
#> mgs:v5.0.0/multiplayer/timer_display
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Convert ticks to seconds
execute store result score #_timer_sec mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #_timer_sec mgs.data /= #20 mgs.data
execute store result score #_timer_min mgs.data run scoreboard players get #_timer_sec mgs.data
scoreboard players operation #_timer_min mgs.data /= #60 mgs.data
scoreboard players operation #_timer_mod mgs.data = #_timer_sec mgs.data
scoreboard players operation #_timer_mod mgs.data %= #60 mgs.data

# Display (only show when < 30 seconds remain as warning)
execute if score #_timer_sec mgs.data matches ..30 as @a[scores={mgs.mp.in_game=1}] run title @s actionbar [{"text":"⏱ ","color":"red"},{"score":{"name":"#_timer_sec","objective":"mgs.data"},"color":"red"},{"text":"s","color":"red"}]

