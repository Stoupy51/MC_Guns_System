
#> mgs:v5.0.0/multiplayer/oob_kill
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/game_tick [ at @s ]
#

# Clear attacker input (environmental death) and simulate death
data modify storage mgs:input with set value {}
function mgs:v5.0.0/multiplayer/simulate_death

