
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_defused
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused","color":"aqua","bold":true}]
kill @e[tag=mgs.snd_bomb]
function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

