
#> mgs:v5.1.0/utils/signal_and_damage_plain
#
# @executed	at @s
#
# @within	mgs:v5.1.0/projectile/damage_entity
#

# Check if target is a player in an active game and damage would be lethal -> simulate death
# (missions needs the state check: mi.in_game is an opt-in flag that is already set in the lobby)
execute store result score #incoming_dmg mgs.data run data get storage mgs:input with.amount 10
execute store result score #victim_hp mgs.data run data get entity @s Health 10
execute if entity @s[type=player,scores={mgs.mp.in_game=1..}] if score #incoming_dmg mgs.data >= #victim_hp mgs.data run return run function mgs:v5.1.0/multiplayer/simulate_death
execute if data storage mgs:missions game{state:"active"} if entity @s[type=player,scores={mgs.mi.in_game=1..}] if score #incoming_dmg mgs.data >= #victim_hp mgs.data run return run function mgs:v5.1.0/missions/simulate_death

# Non-lethal or non-MP: plain damage + signals
function mgs:v5.1.0/utils/damage_plain with storage mgs:input with
function #mgs:signals/damage with storage mgs:input with

