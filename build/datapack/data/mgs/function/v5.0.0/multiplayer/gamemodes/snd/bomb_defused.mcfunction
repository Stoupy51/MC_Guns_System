
#> mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_defused
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/try_defuse
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.bomb_defused","color":"aqua","bold":true}]
kill @e[tag=mgs.snd_bomb]
function mgs:v5.0.0/multiplayer/gamemodes/snd/defenders_win

