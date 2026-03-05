
#> mgs:v5.0.0/multiplayer/gamemodes/snd/cleanup
#
# @within	mgs:v5.0.0/multiplayer/stop
#

kill @e[tag=mgs.snd_obj]
kill @e[tag=mgs.snd_bomb]
tag @a remove mgs.snd_alive

