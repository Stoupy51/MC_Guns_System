
#> mgs:v5.1.0/multiplayer/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Already in death spectate -> this vanilla death was already processed as a simulated death
# (prevents double kill/death messages when a bullet kill and the vanilla death land on the same tick)
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Increment death stats
scoreboard players add @s mgs.mp.deaths 1

# Death message: try to find attacker, otherwise random message
tag @s add mgs.temp_victim
execute on attacker run tag @s add mgs.temp_killer
execute if entity @a[tag=mgs.temp_killer] run function mgs:v5.1.0/multiplayer/random_kill_message
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.1.0/multiplayer/random_death_message
tag @s remove mgs.temp_victim

# Enter death spectate (shared flow: S&D branch, spectator mode, spectate killer/random, titles)
function mgs:v5.1.0/multiplayer/enter_death_spectate

