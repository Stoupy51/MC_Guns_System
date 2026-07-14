
#> mgs:v5.1.0/multiplayer/simulate_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/utils/signal_and_damage
#			mgs:v5.1.0/utils/signal_and_damage_plain
#			mgs:v5.1.0/multiplayer/bounds_kill
#			mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes [ at @e[tag=mgs.snd_bomb] & as @a[distance=..10,gamemode=!creative,scores={mgs.mp.in_game=1..}] ]
#

# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s mgs.mp.deaths 1

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage mgs:input with.amount run function #mgs:signals/damage with storage mgs:input with

# Fire kill signal as attacker (if attacker exists in input)
execute if data storage mgs:input with.attacker run function mgs:v5.1.0/multiplayer/simulate_death_fire_kill with storage mgs:input with

# No attacker: random funny self-death message
execute unless data storage mgs:input with.attacker run function mgs:v5.1.0/multiplayer/random_death_message

# Enter death spectate (shared with vanilla-death on_respawn)
function mgs:v5.1.0/multiplayer/enter_death_spectate

