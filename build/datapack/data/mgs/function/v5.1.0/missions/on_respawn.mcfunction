
#> mgs:v5.1.0/missions/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Already in death spectate -> this vanilla death was already processed as a simulated death
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Increment mission death stats
scoreboard players add @s mgs.mi.deaths 1
scoreboard players set @s mgs.mi.died_here 0

function mgs:v5.1.0/missions/enter_death_spectate

