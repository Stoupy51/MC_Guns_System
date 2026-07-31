
#> mgs:v5.1.0/multiplayer/gamemodes/demo/overtime_expired
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/tick
#

execute unless score #demo_round_active mgs.data matches 1 run return fail
scoreboard players set #demo_round_active mgs.data 0

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚡ ",{"translate":"mgs.overtime_expired_nobody_detonated_the_site","color":"gray"}]
function mgs:v5.1.0/multiplayer/game_draw

