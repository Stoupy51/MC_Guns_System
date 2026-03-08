
#> mgs:v5.0.0/multiplayer/timer_display
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Convert ticks to seconds
execute store result score #timer_sec mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #timer_sec mgs.data /= #20 mgs.data
execute store result score #timer_min mgs.data run scoreboard players get #timer_sec mgs.data
scoreboard players operation #timer_min mgs.data /= #60 mgs.data
scoreboard players operation #timer_mod mgs.data = #timer_sec mgs.data
scoreboard players operation #timer_mod mgs.data %= #60 mgs.data

# Zero-padded seconds for sidebar
scoreboard players operation #timer_tens mgs.data = #timer_mod mgs.data
scoreboard players operation #timer_tens mgs.data /= #10 mgs.data
scoreboard players operation #timer_ones mgs.data = #timer_mod mgs.data
scoreboard players operation #timer_ones mgs.data %= #10 mgs.data

# Refresh sidebar with updated values
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run function #bs.sidebar:refresh {objective:"mgs.sidebar"}
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/refresh_sidebar_ffa

