
#> mgs:v5.0.0/multiplayer/bounds_kill
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/check_bounds
#

# Clear attacker input (environmental death) and simulate death
data modify storage mgs:input with set value {}
function mgs:v5.0.0/multiplayer/simulate_death

