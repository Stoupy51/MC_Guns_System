
#> mgs:v5.3.0/multiplayer/gamemodes/snd/drop_bomb
#
# @executed	at @s
#
# @within	mgs:v5.3.0/multiplayer/gamemodes/snd/on_death
#

tag @s remove mgs.snd_carrier
execute at @e[tag=mgs.snd_carrier_label,limit=1] run function mgs:v5.3.0/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag=mgs.snd_carrier_label]
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"💣 ","color":"white"},{"translate":"mgs.the_bomb_carrier_is_down","fallback":"The bomb carrier is down!","color":"yellow"}]

