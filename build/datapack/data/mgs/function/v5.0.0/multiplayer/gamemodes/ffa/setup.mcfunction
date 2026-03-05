
#> mgs:v5.0.0/multiplayer/gamemodes/ffa/setup
#
# @within	mgs:v5.0.0/multiplayer/start
#

# Reset all teams (no teams in FFA)
team leave @a
scoreboard players set @a mgs.mp.team 0
tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.free_for_all_everyone_for_themselves","color":"yellow"}]

