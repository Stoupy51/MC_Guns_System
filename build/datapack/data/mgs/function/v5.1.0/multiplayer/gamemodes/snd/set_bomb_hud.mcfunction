
#> mgs:v5.1.0/multiplayer/gamemodes/snd/set_bomb_hud
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/update_bomb_hud with storage mgs:temp _snd_hud
#
# @args		sec (unknown)
#

$data modify entity @e[tag=mgs.snd_bomb_hud,limit=1] text set value [{"text":"💣 ","color":"red","bold":true},{"text":"$(sec)s","color":"white"}]

