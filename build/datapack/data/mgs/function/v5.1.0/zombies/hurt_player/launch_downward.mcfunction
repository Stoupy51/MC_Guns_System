
#> mgs:v5.1.0/zombies/hurt_player/launch_downward
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/hurt_player/on_hurt
#

# Launch player downward to counter the slight jump boost from knockback.
scoreboard players set $x player_motion.api.launch 0
scoreboard players set $y player_motion.api.launch -5000
scoreboard players set $z player_motion.api.launch 0
function player_motion:api/launch_xyz

