
#> mgs:v5.0.0/multiplayer/gamemodes/hp/rotate
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/tick
#

# Remove the first entry (current zone) from the zones list
data remove storage mgs:multiplayer game.hp_zones[0]

# Check if there are more zones
execute unless data storage mgs:multiplayer game.hp_zones[0] run function mgs:v5.0.0/multiplayer/gamemodes/hp/reset_zones

# Reset rotation timer
scoreboard players set #hp_rotate_timer mgs.data 1200
scoreboard players set #hp_rotate_sec mgs.data 60

# Load next zone
function mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone

