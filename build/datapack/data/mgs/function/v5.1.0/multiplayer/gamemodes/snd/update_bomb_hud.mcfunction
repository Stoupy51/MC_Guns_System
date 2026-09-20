
#> mgs:v5.1.0/multiplayer/gamemodes/snd/update_bomb_hud
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

scoreboard players operation #snd_bomb_sec_shown mgs.data = #snd_bomb_sec mgs.data
execute store result storage mgs:temp _snd_hud.sec int 1 run scoreboard players get #snd_bomb_sec mgs.data
function mgs:v5.1.0/multiplayer/gamemodes/snd/set_bomb_hud with storage mgs:temp _snd_hud

