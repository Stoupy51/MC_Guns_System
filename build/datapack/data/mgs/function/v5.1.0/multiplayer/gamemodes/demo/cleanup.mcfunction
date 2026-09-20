
#> mgs:v5.1.0/multiplayer/gamemodes/demo/cleanup
#
# @within	mgs:v5.1.0/multiplayer/stop
#

schedule clear mgs:v5.1.0/multiplayer/gamemodes/demo/start_round
execute at @e[tag=mgs.demo_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag=mgs.demo_obj]
kill @e[tag=mgs.demo_label]
kill @e[tag=mgs.demo_bomb]
kill @e[tag=mgs.demo_bomb_vis]
kill @e[tag=mgs.demo_bomb_hud]
kill @e[tag=mgs.demo_wreck]
kill @e[tag=mgs.demo_rubble]
tag @a remove mgs.demo_atk
scoreboard players set #demo_round_active mgs.data 0

