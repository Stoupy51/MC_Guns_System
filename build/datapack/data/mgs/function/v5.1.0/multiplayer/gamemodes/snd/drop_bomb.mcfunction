
#> mgs:v5.1.0/multiplayer/gamemodes/snd/drop_bomb
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/on_death
#

tag @s remove mgs.snd_carrier
execute at @e[tag=mgs.snd_carrier_label,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag=mgs.snd_carrier_label]
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.the_bomb_carrier_is_down","color":"yellow"}]

