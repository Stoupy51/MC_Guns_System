
#> mgs:v5.1.0/multiplayer/gamemodes/snd/recover_bomb
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

execute at @e[tag=mgs.snd_carrier_label,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag=mgs.snd_carrier_label]
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.the_bomb_carrier_left_the_game_bomb_dropped","color":"yellow"}]

