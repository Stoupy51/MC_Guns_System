
#> mgs:v5.1.0/multiplayer/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players set @s mgs.mp.death_count 0

# Already spectating: this vanilla death was handled as a simulated death in the same tick.
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

scoreboard players add @s mgs.mp.deaths 1

# Vanilla damage kills land here, melee included (knives are an attack_damage attribute, not a raycast),
# so the kill is credited through signals/on_kill like a bullet kill.
tag @s add mgs.temp_victim
execute on attacker run tag @s add mgs.temp_killer

# Self-damage: no kill credit, and the fall-through prints a self-death message.
execute if entity @s[tag=mgs.temp_killer] run tag @s remove mgs.temp_killer

execute if entity @a[tag=mgs.temp_killer] run function mgs:v5.1.0/multiplayer/vanilla_kill_credit
execute unless entity @a[tag=mgs.temp_killer] run function mgs:v5.1.0/multiplayer/random_death_message
tag @s remove mgs.temp_victim

function mgs:v5.1.0/multiplayer/enter_death_spectate

