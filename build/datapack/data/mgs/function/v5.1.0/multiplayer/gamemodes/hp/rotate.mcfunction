
#> mgs:v5.1.0/multiplayer/gamemodes/hp/rotate
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/hp/tick
#

data remove storage mgs:multiplayer game.hp_zones[0]

execute unless data storage mgs:multiplayer game.hp_zones[0] run function mgs:v5.1.0/multiplayer/gamemodes/hp/reset_zones

scoreboard players set #hp_rotate_timer mgs.data 1200
scoreboard players set #hp_rotate_sec mgs.data 60

function mgs:v5.1.0/multiplayer/gamemodes/hp/load_zone

