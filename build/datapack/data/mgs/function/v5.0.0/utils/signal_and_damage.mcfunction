
#> mgs:v5.0.0/utils/signal_and_damage
#
# @executed	at @s
#
# @within	mgs:v5.0.0/raycast/deal_damage
#			mgs:v5.0.0/projectile/explode [ as @n[tag=...] ]
#			mgs:v5.0.0/projectile/damage_entity
#

# Check if target is a player in active MP game and damage would be lethal -> simulate death
execute store result score #incoming_dmg mgs.data run data get storage mgs:input with.amount 10
execute store result score #victim_hp mgs.data run data get entity @s Health 10
execute if entity @s[type=player,scores={mgs.mp.in_game=1..}] if score #incoming_dmg mgs.data >= #victim_hp mgs.data run return run function mgs:v5.0.0/multiplayer/simulate_death

# Non-lethal or non-MP: normal damage + signals
function mgs:v5.0.0/utils/damage with storage mgs:input with
function #mgs:signals/damage with storage mgs:input with

