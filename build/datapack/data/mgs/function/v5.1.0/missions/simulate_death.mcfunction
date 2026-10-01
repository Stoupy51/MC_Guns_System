
#> mgs:v5.1.0/missions/simulate_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/utils/signal_and_damage
#			mgs:v5.1.0/utils/signal_and_damage_plain
#

# A second bullet in the same tick, or an OOB kill on top of one.
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Healed so the player never really dies.
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mi.deaths 1

# Hit effects, hitmarker and DPS, for hits.
execute if data storage mgs:input with.amount run function #mgs:signals/damage with storage mgs:input with

# No vanilla death: the body is still where it fell, so the camera stays there instead of snapping to a teammate.
scoreboard players set @s mgs.mi.died_here 1

function mgs:v5.1.0/missions/enter_death_spectate

