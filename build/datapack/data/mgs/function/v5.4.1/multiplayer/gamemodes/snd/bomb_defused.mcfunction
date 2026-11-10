
#> mgs:v5.4.1/multiplayer/gamemodes/snd/bomb_defused
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/snd/tick
#

tellraw @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"💣 ","color":"white"},{"translate":"mgs.bomb_defused","fallback":"BOMB DEFUSED!","color":"aqua","bold":true}]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"💣 ","color":"white"},{"translate":"mgs.bomb_defused","fallback":"BOMB DEFUSED!","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.4.1/progression/mp/award_bomb_defuse
kill @e[tag=mgs.snd_bomb]
function mgs:v5.4.1/multiplayer/gamemodes/snd/defenders_win

