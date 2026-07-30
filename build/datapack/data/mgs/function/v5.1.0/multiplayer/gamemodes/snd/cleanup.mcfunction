
#> mgs:v5.1.0/multiplayer/gamemodes/snd/cleanup
#
# @within	mgs:v5.1.0/multiplayer/stop
#

schedule clear mgs:v5.1.0/multiplayer/gamemodes/snd/start_round
execute at @e[tag=mgs.snd_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag=mgs.snd_obj]
kill @e[tag=mgs.snd_label]
kill @e[tag=mgs.snd_bomb]
kill @e[tag=mgs.snd_bomb_vis]
kill @e[tag=mgs.snd_bomb_hud]
tag @a remove mgs.snd_alive
scoreboard players set #snd_round_active mgs.data 0

