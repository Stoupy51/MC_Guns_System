
#> mgs:v5.1.0/multiplayer/gamemodes/ffa/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

# Only red and blue leave: players stay on mgs.ffa, which hides nametags and enables friendly fire.
team leave @a[team=mgs.red]
team leave @a[team=mgs.blue]
scoreboard players set @a mgs.mp.team 0
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.free_for_all_everyone_for_themselves","color":"yellow"}]

