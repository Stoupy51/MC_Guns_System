
#> mgs:v5.1.0/missions/simulate_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/utils/signal_and_damage
#			mgs:v5.1.0/utils/signal_and_damage_plain
#

# Ignore duplicate deaths (a second bullet landing in the same tick, or an OOB kill on top of one)
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Heal to prevent the actual death & Increment mission death stats
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mi.deaths 1

# Fire the damage signal (hit effects, hitmarker, DPS) if this came from a hit
execute if data storage mgs:input with.amount run function #mgs:signals/damage with storage mgs:input with

# No vanilla death happened, so the body is still standing where it fell: the spectate flow below
# leaves the camera right there instead of snapping to a teammate
scoreboard players set @s mgs.mi.died_here 1

function mgs:v5.1.0/missions/enter_death_spectate

