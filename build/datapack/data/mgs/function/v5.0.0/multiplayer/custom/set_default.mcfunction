
#> mgs:v5.0.0/multiplayer/custom/set_default
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1500

# Store as player's default (scoreboard)
scoreboard players operation @s mgs.mp.default = #loadout_id mgs.data

# Notify
tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.default_loadout_set_it_will_auto_apply_when_a_game_starts","color":"green"}]

