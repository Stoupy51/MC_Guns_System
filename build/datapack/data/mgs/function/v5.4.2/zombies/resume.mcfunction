
#> mgs:v5.4.2/zombies/resume
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/suspended_tick
#

function mgs:v5.4.2/zombies/unfreeze_world
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_game_resumes","fallback":"The game resumes!","color":"green"}]

