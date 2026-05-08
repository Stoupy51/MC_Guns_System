
#> mgs:v5.0.1/multiplayer/gamemodes/snd/cleanup
#
# @within	mgs:v5.0.1/multiplayer/stop
#

execute at @e[tag=mgs.snd_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag=mgs.snd_obj]
kill @e[tag=mgs.snd_bomb]
tag @a remove mgs.snd_alive

