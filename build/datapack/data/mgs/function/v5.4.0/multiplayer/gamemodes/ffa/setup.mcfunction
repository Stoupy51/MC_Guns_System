
#> mgs:v5.4.0/multiplayer/gamemodes/ffa/setup
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/start
#

# Only red and blue leave: players stay on mgs.ffa, which hides nametags and enables friendly fire.
team leave @a[team=mgs.red]
team leave @a[team=mgs.blue]
scoreboard players set @a[scores={mgs.mp.in_game=1}] mgs.mp.team 0
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.free_for_all_everyone_for_themselves","fallback":"Free-For-All! Everyone for themselves!","color":"yellow"}]

