
#> mgs:v5.1.0/multiplayer/simulate_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/utils/signal_and_damage
#			mgs:v5.1.0/utils/signal_and_damage_plain
#			mgs:v5.1.0/multiplayer/bounds_kill
#			mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes [ at @e[tag=mgs.snd_bomb] & as @a[distance=..10,gamemode=!creative,scores={mgs.mp.in_game=1..}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed [ as @a[distance=..8.0,gamemode=!creative,scores={mgs.mp.in_game=1..}] ]
#

# A second bullet, OOB or vanilla death in the same tick.
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Healed so the player never really dies.
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mp.deaths 1

# `mgs:input with` is shared scratch that the signals below reuse (Scavenger refills, lore rewrites clear it),
# so the branch is decided on a score taken now and the signals get a private copy.
execute store success score #mp_death_attacked mgs.data if data storage mgs:input with.attacker
data modify storage mgs:temp _mp_death set from storage mgs:input with

# raycast/apply_damage sets `input with.headshot`. Read into a score because the key is absent for non-bullet deaths,
# and a macro naming a missing key fails the whole function.
scoreboard players set #mp_kill_headshot mgs.data 0
execute store result score #mp_kill_headshot mgs.data run data get storage mgs:temp _mp_death.headshot

# Hit effects, hitmarker and DPS, for bullet hits.
execute if data storage mgs:temp _mp_death.amount run function #mgs:signals/damage with storage mgs:temp _mp_death

execute if score #mp_death_attacked mgs.data matches 1 run function mgs:v5.1.0/multiplayer/simulate_death_fire_kill with storage mgs:temp _mp_death

# No attacker: a random self-death message.
execute if score #mp_death_attacked mgs.data matches 0 run function mgs:v5.1.0/multiplayer/random_death_message

# Shared with vanilla deaths (on_respawn).
function mgs:v5.1.0/multiplayer/enter_death_spectate

