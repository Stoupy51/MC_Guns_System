
#> mgs:v5.1.0/multiplayer/simulate_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/utils/signal_and_damage
#			mgs:v5.1.0/utils/signal_and_damage_plain
#			mgs:v5.1.0/multiplayer/bounds_kill
#			mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes [ at @e[tag=mgs.snd_bomb] & as @a[distance=..10,gamemode=!creative,scores={mgs.mp.in_game=1..}] ]
#

# Ignore duplicate deaths (second bullet / OOB / vanilla death landing in the same tick as another death)
execute if score @s mgs.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mp.deaths 1

# `mgs:input with` is GLOBAL scratch: the signals fired below reuse it (the killer's Scavenger perk
# refills their magazines, and every lore rewrite clears `input with`), so re-reading it after
# a signal used to lose the attacker and print an unattributed death message on top of the kill
# message. Decide the branch on a score taken now, and pass the signals a private copy.
execute store success score #mp_death_attacked mgs.data if data storage mgs:input with.attacker
data modify storage mgs:temp _mp_death set from storage mgs:input with

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage mgs:temp _mp_death.amount run function #mgs:signals/damage with storage mgs:temp _mp_death

# Fire kill signal as attacker (if attacker exists in input)
execute if score #mp_death_attacked mgs.data matches 1 run function mgs:v5.1.0/multiplayer/simulate_death_fire_kill with storage mgs:temp _mp_death

# No attacker: random funny self-death message
execute if score #mp_death_attacked mgs.data matches 0 run function mgs:v5.1.0/multiplayer/random_death_message

# Enter death spectate (shared with vanilla-death on_respawn)
function mgs:v5.1.0/multiplayer/enter_death_spectate

