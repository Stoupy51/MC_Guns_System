
#> mgs:v5.0.0/multiplayer/gamemodes/hp/reset_zones
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/rotate
#

# Refill zones from map data
data modify storage mgs:multiplayer game.hp_zones set from storage mgs:multiplayer game.map.hardpoint
scoreboard players set #hp_zone_idx mgs.data 0

