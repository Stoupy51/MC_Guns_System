
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_defused
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused","color":"aqua","bold":true}]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/mp/award_bomb_defuse
kill @e[tag=mgs.snd_bomb]
function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

